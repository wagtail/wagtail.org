from django import forms
from django.conf import settings

requires_token = not settings.GITHUB_ROADMAP_ACCESS_TOKEN


class ImportForm(forms.Form):
    github_token = forms.CharField(
        max_length=64,
        required=requires_token,
        label="GitHub access token",
        help_text=(
            "Optional — if not supplied, a default token will be used"
            if not requires_token
            else None
        ),
    )
