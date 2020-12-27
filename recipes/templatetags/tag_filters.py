
from django import template

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter(name="get_filter_values")
def get_filter_values(value):
        return value.getlist('filters')

@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
        rq = request.GET.copy()
        if tag != False:
                if tag.slug in request.GET.getlist("filters"):
                        filters = rq.getlist("filters")
                        filters.remove(tag.slug)
                        rq.setlist("filters", filters)
                else:
                        rq.appendlist("filters", tag.slug)
                return rq.urlencode()
        L = rq.urlencode()
        #print(f'L = {L}')
        #print(L.find('filters'), L[L.find('filters'):])
        #print(f"QQQQQQQQQQQQQQQQQQQQQQQQQ {'&'.join(L.split('filters')[1:])}")
        #return "&".join(L.split('&')[1:])
        return  L[L.find('filters'):]