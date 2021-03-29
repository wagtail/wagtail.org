from django.conf import settings
from django.core.files.storage import get_storage_class
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks
from wagtail.core.whitelist import allow_without_attributes
from wagtail.documents import get_document_model
from wagtail.documents.models import document_served

from storages.backends.s3boto3 import S3Boto3Storage


def editor_js():
    js_files = ["js/vendor/hallo-code.js"]
    js_includes = format_html_join(
        "\n",
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files),
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('halloheadings');
            registerHalloPlugin('hallocode');
        </script>
        """
    )


hooks.register("insert_editor_js", editor_js)


def editor_css():
    return format_html(
        '<link rel="stylesheet" href="'
        + settings.STATIC_URL
        + 'css/vendor/fontawesome-free-5.15.3-web/css/all.min.css">'
    )


hooks.register("insert_editor_css", editor_css)


@hooks.register("construct_whitelister_element_rules")
def whitelister_element_rules():
    return {
        "blockquote": allow_without_attributes,
        "pre": allow_without_attributes,
        "code": allow_without_attributes,
    }


# It's important that this hooks runs after all the other hooks,
# hence order is set to "100".
@hooks.register("before_serve_document", order=100)
def serve_document_from_s3(document, request):
    """
    Download document from S3.

    This is to avoid reading the whole document by the Wagtail view
    and potentially risking DoS attack and the server timing out.
    """
    # Skip this hook if not using django-storages boto3 backend.
    if not issubclass(get_storage_class(), S3Boto3Storage):
        return

    # Send document_served signal, same as Wagtail does.
    # https://github.com/wagtail/wagtail/blob/7938e81ab48327a084ac1dced9474c998fd44c2d/wagtail/documents/views/serve.py#L32-L33
    document_served.send(
        sender=get_document_model(), instance=document, request=request
    )

    # Service file directly from S3.
    file_url = document.file.url

    # Generate redirect response and add never_cache headers.
    # Delete all existing headers.
    response = redirect(file_url)
    del response["Cache-control"]
    add_never_cache_headers(response)
    return response
