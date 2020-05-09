from django import template
register = template.Library()

@register.filter(name="get_dict_value")
def get_dict_value(dictionary, key):
    # TODO: check if exists
    return dictionary.get(key, '')
