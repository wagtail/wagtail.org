from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.core import hooks
from wagtail.core.whitelist import allow_without_attributes


def editor_js():
    js_files = [
        'js/vendor/hallo-code.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('halloheadings');
            registerHalloPlugin('hallocode');
        </script>
        """
    )

hooks.register('insert_editor_js', editor_js)


def editor_css():
    return format_html('<link rel="stylesheet" href="' + settings.STATIC_URL + 'css/vendor/font-awesome.min.css">')

hooks.register('insert_editor_css', editor_css)


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'blockquote': allow_without_attributes,
        'pre': allow_without_attributes,
        'code': allow_without_attributes,
    }
