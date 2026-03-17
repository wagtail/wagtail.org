from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView


class SecurityView(TemplateView):
    template_name = "security.txt"
    content_type = "text/plain"

    expires = timedelta(days=7)

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "security_txt": self.request.build_absolute_uri(self.request.path),
            "expires": (timezone.now() + self.expires)
            .replace(microsecond=0)
            .isoformat(),
        }
