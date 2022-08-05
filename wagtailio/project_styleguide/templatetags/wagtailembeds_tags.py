from wagtail.embeds.templatetags.wagtailembeds_tags import register

from pattern_library.monkey_utils import override_tag

override_tag(register, name="embed")
