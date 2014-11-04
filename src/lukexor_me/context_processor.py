from django.conf import settings


def global_vars(request):
    """Returns a dict of variables
    """
    globals = {
        'GA_CODE': settings.GA_CODE,
        'URLS': settings.URLS,
        'STRINGS': settings.STRINGS,
    }

    return globals
