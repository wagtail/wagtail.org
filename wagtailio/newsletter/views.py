from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render

from wagtailio.newsletter.models import NewsletterEmailAddress


@require_POST
def newsletter_signup(request):
    success = False
    try:
        email = request.POST.get('email', '')
        validate_email(email)
        nea = NewsletterEmailAddress()
        nea.email = email
        nea.save()
        success = True
    except ValidationError:
        pass
    return render(request, 'core/newsletter_thanks.html', {
        'success': success
    })
