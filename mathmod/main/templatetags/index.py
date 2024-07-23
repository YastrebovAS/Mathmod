from django import template


register = template.Library()


@register.filter
def index(indexable, i):  # небольшой фильтр, чтобы можно было делать несколько вложенных циклов for в шаблонах(html)
    return indexable[i]
