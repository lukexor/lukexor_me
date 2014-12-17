from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from lukexor_me import settings

def expire_view_cache(
    view_name,
    args=[],
    namespace=None,
    key_prefix=None,
    method="GET"):
    """
    This function allows you to invalidate any view-level cache.

    view_name: view function you wish to invalidate or it's named url pattern
    args: any arguments passed to the view function
    namepace: optioal, if an application namespace is needed
    key prefix: for the @cache_page decorator for the function (if any)
    """

    request = HttpRequest()
    request.method = method
    request.META = { 'HTTP_HOST': settings.DOMAIN_NAME }

    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)

    key = get_cache_key(request, key_prefix=settings.CACHES['default']['KEY_PREFIX'])

    if key:
        if cache.get(key):
            cache.delete(key)
        return True
    return False

