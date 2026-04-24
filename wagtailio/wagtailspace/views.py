from pathlib import Path

from django.http import Http404
from django.template.response import TemplateResponse
from django.views import View


SPACE_2025_ROOT = (
    Path(__file__).resolve().parent
    / "templates"
    / "wagtailspace"
    / "wagtail-space-2025"
)


class WagtailSpace2025View(View):
    def get(self, request, asset_path="index.html"):
        # Default directory request to index
        if not asset_path or asset_path.endswith("/"):
            asset_path = f"{asset_path}index.html" if asset_path else "index.html"

        target = (SPACE_2025_ROOT / asset_path).resolve()

        # Prevent ../ traversal and ensure file exists
        if SPACE_2025_ROOT not in target.parents and target != SPACE_2025_ROOT:
            raise Http404()
        if not target.is_file():
            raise Http404()

        return TemplateResponse(request, str(target), {})
