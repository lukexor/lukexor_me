from django import template
from django.conf import settings
from django.utils.http import urlquote

register = template.Library()

@register.filter
def getValueByKey(arg, key):
    return arg[key]
    collection = ''
    if type(collection) is dict:
        return collection.get(key)
    elif type(collection) in (list, tuple):
        return collection[key] if len(collection) > key else ''
    return ''


@register.simple_tag
def create_share_url(type, base_url, url, text=""):
    """
    Return a url to share a link on social media
    """

    url = base_url + '/' + url
    share_url = ''

    if type == 'twitter':
        share_url = share_url + settings.URLS['share_twitter'] % (url, urlquote(text))
    elif type == 'facebook':
        share_url = share_url + settings.URLS['share_facebook'] % (url)
    elif type == 'google':
        share_url = share_url + settings.URLS['share_google'] % (url)

    return share_url
