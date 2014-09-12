from django import template

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
