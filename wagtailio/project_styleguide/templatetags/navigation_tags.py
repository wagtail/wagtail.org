from pattern_library.monkey_utils import override_tag

from wagtailio.core.templatetags.navigation_tags import register

override_tag(register, name="footer_navigation")
