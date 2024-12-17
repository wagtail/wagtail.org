from pattern_library.monkey_utils import override_tag
from wagtail.embeds.templatetags.wagtailembeds_tags import register


override_tag(register, name="embed")
