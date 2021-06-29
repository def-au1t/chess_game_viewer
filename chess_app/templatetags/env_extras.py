from django import template
import os

register = template.Library()


@register.simple_tag(name="get_env")
def get_env(key):
    return os.environ.get(key, 'Baza partii szachowych')
