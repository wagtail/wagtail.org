from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap


class Sitemap(WagtailSitemap):
    def items(self):
        # No need for a .specific() call
        # Note, if modifying the get_sitemap_urls() method on any of the custom page
        # types, then you need to re-add .defer_streamfields().specific() at the end of
        # this call, or better yet, default back to Wagtail's sitemap
        return (
            self.get_wagtail_site()
            .root_page.get_descendants(inclusive=True)
            .live()
            .public()
            .order_by("path")
        )
