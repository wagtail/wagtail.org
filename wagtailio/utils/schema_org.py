from django.core.cache import cache

from wagtailio.core.models.settings import OrganisationSchemaSettings


def get_organisation_schema() -> dict | None:
    if organisation := cache.get("organisation_schema"):
        return organisation

    try:
        settings = OrganisationSchemaSettings.objects.get()
    except OrganisationSchemaSettings.DoesNotExist:
        return None

    organisation = settings.to_schema_dict()
    cache.set("organisation_schema", organisation)
    return organisation


def breadcrumbs_schema(page, request=None, extra_items=None):
    crumbs = [
        (ancestor.title, ancestor.get_full_url(request))
        for ancestor in page.get_ancestors(inclusive=True)
        if not ancestor.is_root()
    ]
    crumbs += [(extra.get("title"), extra.get("url")) for extra in extra_items or []]

    if len(crumbs) < 2:
        return {}

    items = []
    for position, (name, url) in enumerate(crumbs, start=1):
        item = {"@type": "ListItem", "position": position, "name": name}
        # The last crumb is the current page; Google omits its URL.
        if position < len(crumbs):
            item["item"] = url
        items.append(item)

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }
