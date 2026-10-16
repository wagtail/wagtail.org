from wagtail.models import Page


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
