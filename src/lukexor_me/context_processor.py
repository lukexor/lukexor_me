from django.conf import settings


def global_vars(request):
    """Returns a dict of variables
    """
    globals = {
        'SITE_SUBTITLE': settings.SITE_SUBTITLE,
        'GA_CODE': settings.GA_CODE,
        'URLS': settings.URLS,
    }

    return globals
