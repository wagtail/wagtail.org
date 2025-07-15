from datetime import datetime
from io import BytesIO
from pprint import pprint

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from bs4 import BeautifulSoup, Tag
import requests
import willow

from wagtailio.images.models import WagtailIOImage
from wagtailio.newsletter.models import NewsletterIndexPage, NewsletterPage


def clean_tag(tag):
    if tag.name == "a":
        href = tag.get("href", "")
        tag.attrs = {"href": href} if href else {}
    else:
        tag.attrs = {}
    for child in tag.find_all(True):
        clean_tag(child)
    return tag


def parse_newsletter_html(soup: Tag):
    h1 = soup.select("h1")[0]
    title_tr = h1.findParent("tr")

    while not title_tr.previous_sibling:
        # On issue 160, the title is inside two nested `tr` tags.
        # On issue 187, it's 12 nested `tr` tags deep, hence the loop. Don't ask.
        title_tr = title_tr.findParent("tr")

    tr = title_tr.previous_sibling  # the row that contains the date
    while tr:
        yield tr
        tr = tr.next_sibling


def parse_date(date_str):
    return datetime.strptime(date_str, "%d %B %Y").date()


def get_or_create_image(image_url):
    description = f"newsletter - downloaded from {image_url}"
    existing_image = WagtailIOImage.objects.filter(description=description).first()
    if existing_image:
        return existing_image

    response = requests.get(image_url, timeout=10)
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


def process_block_content(block):
    h1 = block.find("h1")
    if h1:
        return {"type": "heading", "value": h1.get_text().strip()}

    button_table = block.select_one("table.mceButtonContainer") or block.select_one(
        "td.mceButton"
    )
    if button_table:
        link = button_table.find("a")
        if link:
            return {
                "type": "button",
                "value": {
                    "text": link.get_text().strip(),
                    "url": link.get("href", ""),
                },
            }

    img = block.find("img")
    if img and img.get("src"):
        image_url = img.get("src")
        image = get_or_create_image(image_url)
        return {
            "type": "image",
            "value": image.id,
        }

    paragraphs = block.find_all("p")
    if paragraphs:
        cleaned_paragraphs = [clean_tag(p) for p in paragraphs]
        content = "<br/>".join(p.decode_contents() for p in cleaned_paragraphs)
        return {"type": "rich_text", "value": f"<p>{content}</p>"}


def process_newsletter_content(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    newsletter_subject = soup.title.string.strip()
    if newsletter_subject.startswith("This Week in Wagtail:"):
        newsletter_subject = soup.title.string.split(":", 1)[1].strip()

    blocks_iterator = parse_newsletter_html(soup)

    date_block = next(blocks_iterator)
    date_text = date_block.get_text().strip()
    newsletter_date = parse_date(date_text)

    body = []
    for block in blocks_iterator:
        text = block.get_text().strip()
        if text.startswith("Until next time, thank you for reading"):
            break

        if block_content := process_block_content(block):
            body.append(block_content)

    return {
        "date": newsletter_date,
        "body": body,
        "newsletter_subject": newsletter_subject,
    }


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

        newsletter_data = process_newsletter_content(url)
        newsletter_data["title"] = title

        if options["debug"]:
            pprint(newsletter_data["body"])  # noqa: T203

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
