from django.conf import settings
from django.core.cache import cache


def base_context(request):
    """This dictionary is added in the settings as a context_processor,
    making it available in all requests."""
    return {
        'SITE_NAME': settings.SITE_NAME,
    }
