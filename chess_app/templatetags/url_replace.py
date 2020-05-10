from django import template
register = template.Library()

@register.simple_tag(name="url_replace")
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
