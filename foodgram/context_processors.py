from recipes.models import ShoppingList
from django.contrib.auth.decorators import login_required


def purchases_number(request):
    # if ShoppingList.objects.filter(user=request.user).count() > 0:
    #     return {"number": ShoppingList.objects.filter(user=request.user).count()}
    # return {"number": ''}
    if  request.user.is_authenticated:
        return {"number": ShoppingList.objects.filter(user=request.user).count()}
    else:
        return {"number": ''}
