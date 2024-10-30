from django.core.files.storage import get_storage_class
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers

from wagtail import hooks
from wagtail.documents import get_document_model
from wagtail.documents.models import document_served
from wagtail.whitelist import allow_without_attributes

from storages.backends.s3 import S3Storage


@hooks.register("construct_whitelister_element_rules")
def whitelister_element_rules():
    return {
        "blockquote": allow_without_attributes,
        "pre": allow_without_attributes,
        "code": allow_without_attributes,
    }


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/solid/address-card.svg",
        "wagtailfontawesomesvg/solid/bars.svg",
        "wagtailfontawesomesvg/solid/bullhorn.svg",
        "wagtailfontawesomesvg/solid/cube.svg",
        "wagtailfontawesomesvg/solid/envelope-open-text.svg",
        "wagtailfontawesomesvg/solid/gem.svg",
        "wagtailfontawesomesvg/solid/image.svg",
        "wagtailfontawesomesvg/solid/images.svg",
        "wagtailfontawesomesvg/solid/rectangle-list.svg",
        "wagtailfontawesomesvg/solid/newspaper.svg",
        "wagtailfontawesomesvg/solid/table-list.svg",
        "wagtailfontawesomesvg/solid/rocket.svg",
    ]


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
    if not issubclass(get_storage_class(), S3Storage):
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
