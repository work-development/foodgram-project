import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response


from .models import (
    FollowRecipe,
    FollowUser,
    Ingredient,
    Recipe,
    ShoppingList,
    User,
)
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def create(self, request):
        recipe = get_object_or_404(Recipe, id=self.request.data.get("id"))
        FollowRecipe.objects.get_or_create(
            recipe=recipe, user=self.request.user
        )
        recipe.is_favorite = True
        recipe.save()
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data)

    def destroy(self, request, pk):
        favorite_id = pk
        fr = FollowRecipe.objects.filter(
            recipe=favorite_id, user=self.request.user
        )
        recipe = Recipe.objects.get(id=favorite_id)
        recipe.is_favorite = False
        recipe.save()
        fr.delete()
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data)


# Функция передачи вываливающемуся списку (в поле ингридиенты в форме регистрации) ингредиентов
# ассоциированных по первым буквам уже введенной части слова пользователем
def ingredients(request):
    associated_ingredients = list(
        Ingredient.objects.filter(
            title__icontains=request.GET["query"]
        ).values("title", "dimension")
    )
    return JsonResponse(associated_ingredients, safe=False)


@login_required
def subscriptions(request):
    author_id = int(json.loads(request.body).get("id"))
    author = get_object_or_404(User, pk=author_id)
    if (
        request.user.id != author_id
        and FollowUser.objects.filter(user=request.user, author=author).count()
        == 0
    ):
        FollowUser.objects.create(user=request.user, author=author)
    return JsonResponse({"success": True})


@login_required
def subscriptions_delete(request, author_id):
    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, id=author_id)
    follow_user = get_object_or_404(FollowUser, user=user, author=author)
    follow_user.delete()
    return JsonResponse({"success": True})


@login_required
def purchases(request):
    id = int(json.loads(request.body).get("id"))
    recipe = get_object_or_404(Recipe, pk=id)
    if request.user.id != id:
        ShoppingList.objects.create(user=request.user, recipe=recipe)
        return JsonResponse({"success": True})


@login_required
def purchases_delete(request, id):
    user = get_object_or_404(User, username=request.user.username)
    recipe = get_object_or_404(Recipe, id=id)
    shopping_list = get_object_or_404(ShoppingList, user=user, recipe=recipe)
    shopping_list.delete()
    return JsonResponse({"success": True})
