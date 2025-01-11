def monkeypatch_mrml():
    from mjml import mjml2html
    from wagtail_newsletter.templatetags.wagtail_newsletter import (
        MRMLError,
        MRMLRenderNode,
    )

    def render(self, context) -> str:
        mjml_source = self.nodelist.render(context)
        try:
            return mjml2html(mjml_source)

        except Exception as error:  # noqa: B902
            raise MRMLError("Failed to render MJML") from error

    MRMLRenderNode.render = render


monkeypatch_mrml()
