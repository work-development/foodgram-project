from django import template

from recipes.models import FollowUser, ShoppingList

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter(name="follow")
def follow(author, user):
    if FollowUser.objects.filter(user=user, author=author):
        return True
    return False


@register.filter(name="shop")
def shop(recipe, user):
    if user.is_authenticated:
        if ShoppingList.objects.filter(user=user, recipe=recipe):
            return True
    return False


@register.filter(name="subtract")
def subtract(value):
    return value - 3


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def checktag(tag, sample):
    return tag == sample
