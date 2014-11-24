from . import settings


def GlobalVars(request):
    """
    Returns a dict of variables
    """
    globals = {
        'GA_CODE': settings.GA_CODE,
        'URLS': settings.URLS,
        'STRINGS': settings.STRINGS,
    }

    return globals

def BaseURL(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL': scheme + request.get_host(),}
