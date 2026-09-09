from datetime import datetime
import hashlib
from io import BytesIO
from itertools import zip_longest
from pathlib import Path
from pprint import pprint

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
import requests
import willow

from wagtailio.images.models import WagtailIOImage
from wagtailio.newsletter.models import NewsletterIndexPage, NewsletterPage


CACHE_DIR = Path(".newsletter_cache")

# eepurl.com responds with "403 Forbidden" to non-browser user agents
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"

IMAGE_DESCRIPTION_PREFIX = "newsletter - downloaded from "

# Tags that map to StreamField blocks. Anything else (tables, divs, spans)
# is mailchimp layout scaffolding.
CONTENT_TAGS = ["h1", "h2", "h3", "h4", "p", "ul", "ol", "img"]

# The rich text editor stores bold/italic as b/i, and h2 is the only
# heading level enabled in NEWSLETTER_RICHTEXT_FEATURES.
RENAME_TAGS = {"strong": "b", "em": "i", "h3": "h2", "h4": "h2"}

# Invisible characters that appear in mailchimp markup; ignored when
# comparing source text with imported text.
IGNORED_CHARACTERS = (
    "\u200b\u200c\ufeff"  # zero-width space, zero-width non-joiner, BOM
)


def download(url):
    """Fetch a URL, caching the response body on disk.

    The archive import fetches ~80 pages per run; the cache makes re-runs
    (while iterating on the parser) fast.
    """
    cache_file = CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest() + ".html")
    if cache_file.exists():
        return cache_file.read_text()

    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()

    CACHE_DIR.mkdir(exist_ok=True)
    (CACHE_DIR / ".gitignore").write_text("*\n")
    cache_file.write_text(response.text)
    return response.text


def clean_tag(tag):
    """Reduce a tag to the markup the rich text editor would produce."""
    if tag.name in RENAME_TAGS:
        tag.name = RENAME_TAGS[tag.name]
    if tag.name == "a":
        href = tag.get("href", "")
        tag.attrs = {"href": href} if href else {}
    else:
        tag.attrs = {}
    if tag.name == "li":
        # list items contain inline content, not paragraphs
        for p in tag.find_all("p"):
            p.unwrap()
    for span in tag.find_all("span"):
        # the editor doesn't use span; with its attributes stripped it's noise
        span.unwrap()
    for child in tag.find_all(True):
        clean_tag(child)
    return tag


def parse_newsletter_html(soup: Tag):
    h1 = soup.select("h1")[0]
    title_tr = h1.find_parent("tr")

    while not title_tr.previous_sibling:
        # On issue 160, the title is inside two nested `tr` tags.
        # On issue 187, it's 12 nested `tr` tags deep, hence the loop. Don't ask.
        title_tr = title_tr.find_parent("tr")

    tr = title_tr.previous_sibling  # the row that contains the date
    while tr:
        if isinstance(tr, Tag):
            yield tr
        tr = tr.next_sibling


def is_closing_row(row):
    return row.get_text().strip().startswith("Until next time, thank you for reading")


def parse_date(date_str):
    return datetime.strptime(date_str, "%d %B %Y").date()


def get_or_create_image(image_url):
    description = f"{IMAGE_DESCRIPTION_PREFIX}{image_url}"
    existing_image = WagtailIOImage.objects.filter(description=description).first()
    if existing_image:
        return existing_image

    response = requests.get(image_url, headers={"User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()

    filename = image_url.split("/")[-1]

    img_bytes = BytesIO(response.content)
    willow_image = willow.Image.open(img_bytes)
    width, height = willow_image.get_size()

    image = WagtailIOImage(
        title=filename,
        description=description,
        file=ImageFile(BytesIO(response.content), name=filename),
        width=width,
        height=height,
    )
    image.save()
    return image


def is_button_container(tag):
    classes = tag.get("class", [])
    return "mceButtonContainer" in classes or "mceButton" in classes


def find_content_elements(row):
    """Yield the content elements of a row, in document order.

    Finds headings, paragraphs, lists, images and mailchimp buttons,
    skipping anything nested inside another match (the `p` inside a list
    item, the `a` inside a button).
    """

    def match(tag):
        return tag.name in CONTENT_TAGS or is_button_container(tag)

    for element in row.find_all(match):
        if element.find_parent(match) is None:
            yield element


def process_block_content(row):
    """Convert one newsletter row into a list of StreamField blocks.

    Older issues have one piece of content per row, but recent ones pack
    an h1, an image, several paragraphs and sometimes a button into the
    same row, so a row may produce more than one block. Consecutive
    paragraphs, lists and subheadings merge into a single rich_text block.
    """
    blocks = []
    rich_text_parts = []

    def flush_rich_text():
        if rich_text_parts:
            blocks.append({"type": "rich_text", "value": "".join(rich_text_parts)})
            rich_text_parts.clear()

    for element in find_content_elements(row):
        if is_button_container(element):
            link = element.find("a")
            if link:
                flush_rich_text()
                blocks.append(
                    {
                        "type": "button",
                        "value": {
                            "text": link.get_text().strip(),
                            "url": link.get("href", ""),
                            "page": None,
                        },
                    }
                )
        elif element.name == "h1":
            flush_rich_text()
            blocks.append({"type": "heading", "value": element.get_text().strip()})
        elif element.name == "img":
            if element.get("src"):
                flush_rich_text()
                image = get_or_create_image(element["src"])
                blocks.append({"type": "image", "value": image.id})
        elif text_tokens(element.get_text()):
            rich_text_parts.append(str(clean_tag(element)))
        # else: an empty spacer paragraph; skip it

    flush_rich_text()
    return blocks


def process_newsletter_content(soup):
    newsletter_subject = soup.title.string.strip()
    if newsletter_subject.startswith("This Week in Wagtail:"):
        newsletter_subject = newsletter_subject.split(":", 1)[1].strip()

    rows_iterator = parse_newsletter_html(soup)

    date_row = next(rows_iterator)
    newsletter_date = parse_date(date_row.get_text().strip())

    body = []
    for row in rows_iterator:
        if is_closing_row(row):
            break
        body.extend(process_block_content(row))

    accent_packages_section(body)

    return {
        "date": newsletter_date,
        "body": body,
        "newsletter_subject": newsletter_subject,
    }


def accent_packages_section(body):
    """Display the "Packages" section at the bottom as accented rich text.

    Like in the original newsletter, the section heading is part of the
    accented block.
    """
    for position, block in enumerate(body):
        if block["type"] == "heading" and block["value"] == "Packages":
            section = body[position + 1 :]
            if section and all(b["type"] == "rich_text" for b in section):
                parts = ["<h2>Packages</h2>"] + [b["value"] for b in section]
                body[position:] = [
                    {"type": "accent_rich_text", "value": "".join(parts)}
                ]
            return


def text_tokens(text):
    for character in IGNORED_CHARACTERS:
        text = text.replace(character, "")
    return text.split()


def extract_source_tokens(soup):
    """The sequence of words and images in the source newsletter.

    Walks the same rows as the importer, but extracts text and images
    naively, without any block parsing, so that the importer's output can
    be checked against it.
    """
    tokens = []
    rows_iterator = parse_newsletter_html(soup)
    next(rows_iterator)  # the date row is not part of the body
    for row in rows_iterator:
        if is_closing_row(row):
            break
        for element in row.descendants:
            if isinstance(element, Comment):
                continue
            elif isinstance(element, NavigableString):
                if element.find_parent(["style", "script"]) is None:
                    tokens.extend(text_tokens(str(element)))
            elif element.name == "img" and element.get("src"):
                tokens.append(f"[image: {element['src']}]")
    return tokens


def extract_body_tokens(body):
    """The sequence of words and images in a parsed newsletter body."""
    tokens = []
    for block in body:
        if block["type"] == "heading":
            tokens.extend(text_tokens(block["value"]))
        elif block["type"] in ("rich_text", "accent_rich_text"):
            text = BeautifulSoup(block["value"], "html.parser").get_text(" ")
            tokens.extend(text_tokens(text))
        elif block["type"] == "image":
            image = WagtailIOImage.objects.get(id=block["value"])
            url = image.description.removeprefix(IMAGE_DESCRIPTION_PREFIX)
            tokens.append(f"[image: {url}]")
        elif block["type"] == "button":
            tokens.extend(text_tokens(block["value"]["text"]))
    return tokens


def verify_newsletter_content(soup, body):
    """Check that the parsed body has all source text and images, in order.

    Returns an error message, or None if everything matches.
    """
    expected = extract_source_tokens(soup)
    actual = extract_body_tokens(body)
    if expected == actual:
        return None

    for position, (expected_token, actual_token) in enumerate(
        zip_longest(expected, actual)
    ):
        if expected_token != actual_token:
            context = " ".join(expected[max(0, position - 5) : position])
            return (
                f"mismatch at token {position} (after {context!r}): "
                f"expected {expected_token!r}, got {actual_token!r}"
            )


class Command(BaseCommand):
    help = "Import newsletter content from HTML files"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str, help="URL of the newsletter HTML file")
        parser.add_argument("title", type=str, help="Title for the newsletter page")
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Print debug information",
        )

    def handle(self, *args, **options):
        url = options["url"]
        title = options["title"]
        index_page = NewsletterIndexPage.objects.get()

        soup = BeautifulSoup(download(url), "html.parser")
        newsletter_data = process_newsletter_content(soup)
        newsletter_data["title"] = title

        if options["debug"]:
            pprint(newsletter_data["body"])  # noqa: T203

        error = verify_newsletter_content(soup, newsletter_data["body"])
        if error:
            raise CommandError(f"{title}: {error}")

        existing_page = (
            NewsletterPage.objects.child_of(index_page).filter(title=title).first()
        )

        if existing_page:
            existing_page.body = newsletter_data["body"]
            existing_page.newsletter_subject = newsletter_data["newsletter_subject"]
            existing_page.date = newsletter_data["date"]
            existing_page.save_revision().publish()
        else:
            newsletter_page = NewsletterPage(**newsletter_data)

            index_page.add_child(instance=newsletter_page)
            newsletter_page.save_revision().publish()
