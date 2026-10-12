from wagtail.models import Page

from bs4 import BeautifulSoup


def build_page_tree(pages, root, max_levels=3):
    tree = []
    children_by_path = {root.path: tree}

    for page in pages:
        siblings = children_by_path.get(page.path[: -Page.steplen])
        if siblings is None or page.depth - root.depth > max_levels:
            continue

        children = []
        siblings.append({"page": page, "children": children})
        children_by_path[page.path] = children

    return tree


def get_headings(html_fragments):
    tree = []

    for html in html_fragments:
        for heading in BeautifulSoup(html, "html.parser").find_all(
            ["h2", "h3"], id=True
        ):
            item = {"id": heading["id"], "text": heading.get_text(), "children": []}
            if heading.name == "h3" and tree:
                tree[-1]["children"].append(item)
            else:
                tree.append(item)

    return tree
