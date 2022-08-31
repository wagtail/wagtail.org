from django.conf import settings


def global_pages(request):
    return {
        "BASE_URL": getattr(settings, "BASE_URL", ""),
        "DEBUG": getattr(settings, "DEBUG", ""),
        "FB_APP_ID": getattr(settings, "FB_APP_ID", ""),
        "MAILCHIMP_ACCOUNT_ID": getattr(settings, "MAILCHIMP_ACCOUNT_ID", ""),
        "MAILCHIMP_NEWSLETTER_ID": getattr(settings, "MAILCHIMP_NEWSLETTER_ID", ""),
    }
