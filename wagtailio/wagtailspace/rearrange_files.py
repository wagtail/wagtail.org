#!/usr/bin/env python3
"""
Rearrange Wagtail Space 2025 files into the desired project layout.
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil


TARGET_ROOT = Path("wagtailspace")
TARGET_STATIC = TARGET_ROOT / "static" / "wagtailspace"
TARGET_TEMPLATES = TARGET_ROOT / "templates" / "wagtailspace"
EVENT_SLUG = "wagtail-space-2025"
LOGO_NAMES = [
    "bluesky-brands_1.max-100x100.png",
    "github-brands_1.max-100x100.png",
    "mastodon-brands_1.max-100x100.png",
    "youtube-brands_1.max-100x100.png",
    # These were in wagtail.org/wagtailio/static/img; move to wagtailspace archive by hand
    "wagtail-rocketship.png",
    "wagtail-space-stars.png",
    "WagtailSpace2025Logo.png",
]


def ensure_directories() -> None:
    for path in [
        TARGET_STATIC / "css",
        TARGET_STATIC / "fonts",
        TARGET_STATIC / "images",
        TARGET_STATIC / "img",
        TARGET_TEMPLATES,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def get_css_filename(source_event_dir: Path) -> str:
    css_dir = source_event_dir / "static" / "css"
    css_files = sorted(css_dir.glob("*.css"))
    if not css_files:
        raise FileNotFoundError(f"No CSS files found in: {css_dir}")
    return css_files[0].name


def copy_css_file(source_event_dir: Path, css_filename: str) -> None:
    source_css = source_event_dir / "static" / "css" / css_filename
    target_css = TARGET_STATIC / "css" / "wagtailspace-2025.css"
    target_css.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(str(source_css), str(target_css))


def copy_event_templates(source_event_dir: Path) -> Path:
    destination_parent = TARGET_TEMPLATES
    destination = destination_parent / source_event_dir.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source_event_dir, destination)
    return destination


def copy_images() -> None:
    source_images = Path("media.wagtail.org") / "images"
    target_images = TARGET_STATIC / "images" / EVENT_SLUG
    target_images.mkdir(parents=True, exist_ok=True)
    logo_set = set(LOGO_NAMES)

    for image_path in source_images.glob("*"):
        if image_path.is_file() and image_path.name not in logo_set:
            shutil.copy(str(image_path), str(target_images / image_path.name))


def copy_logos() -> None:
    source_images = Path("media.wagtail.org") / "images"
    target_img = TARGET_STATIC / "img" / EVENT_SLUG
    target_img.mkdir(parents=True, exist_ok=True)

    for logo in LOGO_NAMES:
        if (source_images / logo).is_file():
            shutil.copy(str(source_images / logo), str(target_img / logo))


def add_template_load_tag(html: str) -> str:
    load_tag = "{% load static manifest %}"
    if load_tag in html:
        return html
    return f"{load_tag}\n{html}"


def replace_css_href(html: str, css_filename: str) -> str:
    css_link_pattern = re.compile(
        rf'href=["\'](?:(?:\.\./)+|/)?static/css/{re.escape(css_filename)}["\']'
    )
    return css_link_pattern.sub(
        "href=\"{% static 'wagtailspace/css/wagtailspace-2025.css' %}\"",
        html,
    )


def replace_primary_nav_links(html: str) -> str:
    anchor_pattern = re.compile(
        r'<a\s+class="primary-nav__item-container"[^>]*>',
        re.IGNORECASE,
    )
    href_pattern = re.compile(r'href="(?:\.\./)?([^"/]+)/index\.html"')

    def _replace_anchor(match: re.Match[str]) -> str:
        tag = match.group(0)
        return href_pattern.sub(
            lambda href_match: (
                f"href=\"{{% url 'wagtail-space-2025' asset_path='{href_match.group(1)}' %}}\""
            ),
            tag,
        )

    return anchor_pattern.sub(_replace_anchor, html)


def replace_image_references(html: str) -> str:
    image_ref_pattern = re.compile(
        r'src=["\'](?:\.\./)*media\.wagtail\.org/images/([^"\']+)["\']'
    )
    html = image_ref_pattern.sub(
        lambda match: (
            f"src=\"{{% static 'wagtailspace/images/wagtailspace-2025/{match.group(1)}' %}}\""
        ),
        html,
    )
    logo_set = set(LOGO_NAMES)
    static_image_pattern = re.compile(
        r"src=\"\{\% static 'wagtailspace/images/wagtailspace-2025/([^']+)' \%\}\""
    )
    static_img_source_pattern = re.compile(
        r'src=["\'](?:(?:\.\./)+|/)?static/img/([^"\']+)["\']'
    )

    def _reroute_logos(match: re.Match[str]) -> str:
        filename = match.group(1)
        if filename in logo_set:
            return f"src=\"{{% static 'wagtailspace/img/wagtailspace-2025/{filename}' %}}\""
        return match.group(0)

    html = static_image_pattern.sub(_reroute_logos, html)

    def _rewrite_static_img_src(match: re.Match[str]) -> str:
        filename = match.group(1)
        normalized = re.sub(r"\.[0-9a-fA-F]{6,}(?=\.[^.]+$)", "", filename)
        return (
            f"src=\"{{% static 'wagtailspace/img/wagtailspace-2025/{normalized}' %}}\""
        )

    return static_img_source_pattern.sub(_rewrite_static_img_src, html)


def replace_manifest_scripts(html: str) -> str:
    blocking_pattern = re.compile(
        r'<script\s+src="\.\./static/js/blocking\.[^"]+\.js"></script>'
    )
    main_pattern = re.compile(
        r'<script\s+src="\.\./static/js/main\.[^"]+\.js"></script>'
    )

    html = blocking_pattern.sub(
        "<script src=\"{% manifest 'js/blocking.js' %}\"></script>",
        html,
    )
    html = main_pattern.sub(
        "<script src=\"{% manifest 'js/main.js' %}\"></script>",
        html,
    )
    return html


def rewrite_html_files(event_template_dir: Path, css_filename: str) -> None:
    for html_file in event_template_dir.rglob("*.html"):
        original = html_file.read_text(encoding="utf-8")
        updated = original
        updated = add_template_load_tag(updated)
        updated = replace_css_href(updated, css_filename)
        updated = replace_primary_nav_links(updated)
        updated = replace_image_references(updated)
        updated = replace_manifest_scripts(updated)
        if updated != original:
            html_file.write_text(updated, encoding="utf-8")


def main() -> None:
    source_dir = Path("wagtail.org")
    source_event_dir = Path("wagtail.org") / EVENT_SLUG
    if not source_event_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_event_dir}")

    ensure_directories()
    css_filename = get_css_filename(source_dir)
    copy_css_file(source_dir, css_filename)
    moved_event_dir = copy_event_templates(source_event_dir)
    copy_images()
    copy_logos()
    rewrite_html_files(moved_event_dir, css_filename)


if __name__ == "__main__":
    main()
