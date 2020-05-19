from django import template
register = template.Library()


PAGES_BEFORE = 6
PAGES_AFTER = 5

@register.simple_tag(name="page_range")
def page_range(current_page, pages_num):
    return range(max(current_page - PAGES_BEFORE + 1, 1), min(current_page + PAGES_AFTER + 1, pages_num + 1), 1)
