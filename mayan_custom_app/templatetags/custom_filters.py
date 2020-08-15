from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(val, arg):
    return val.split(arg)

@register.filter
def labels(objects):
    return [obj.label for obj in objects]

@register.simple_tag
def first_matching_tag(*filter_list, **kwargs):
    for tag in kwargs['tags']:
        if tag.label in filter_list:
            return tag.label
    return kwargs['default']
