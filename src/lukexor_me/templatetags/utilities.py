from django import template
from django.utils.http import urlquote
from django.core.urlresolvers import reverse_lazy
from lukexor_me import settings

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
def create_share_url(type, base_url, post, permalink_url, text="Good read"):
    """
    Return a url to share a link on social media
    """

    url = "%s%s" % (base_url, create_permalink_url(post, permalink_url))
    share_url = ''

    if type == 'twitter':
        share_url = share_url + settings.URLS['share_twitter'] % (url, urlquote(text))
    elif type == 'facebook':
        share_url = share_url + settings.URLS['share_facebook'] % (url)
    elif type == 'google':
        share_url = share_url + settings.URLS['share_google'] % (url)

    return share_url

@register.simple_tag
def create_permalink_url(post, permalink_url):
    """
    Returns a dated permalink string
    """

    year = None
    month = None

    if post.date_published:
        year = post.date_published.strftime('%Y')
        month = post.date_published.strftime('%m')

    if year and month:
        return reverse_lazy(permalink_url, args=[year, month, post.permalink_title])
    else:
        return ''
