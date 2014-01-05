from django.conf import settings


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {
        'display_version': getattr(settings, 'DISPLAY_VERSION', False),
        'version': getattr(settings, 'VERSION', 'N/A'),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'FACEBOOK_KEY': getattr(settings, 'FACEBOOK_KEY', None),
    }
