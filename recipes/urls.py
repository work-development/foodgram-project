from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api, views
from .api import FavoriteViewSet

router = DefaultRouter()
router.register("favorites", FavoriteViewSet, basename="favorites")

urlpatterns = [
    path("api/", include(router.urls)),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_page"),
    path("new_recipe", views.new_recipe, name="new_recipe"),
    path("subscribe_list", views.subscribe_list, name="subscribe_list"),
    path("favorites_page", views.favorites_page, name="favorites_page"),
    path(
        "shop_list/dowload/",
        views.download_shopping_list,
        name="download_shopping_list",
    ),
    path(
        "shop_list/<int:recipe_id>/",
        views.delete_purchase,
        name="delete_purchase",
    ),
    path("shop_list", views.shop_list, name="shop_list"),
    path("purchases/<int:id>", api.purchases_delete, name="purchases_del"),
    path("purchases", api.purchases, name="purchases"),
    path("ingredients", api.ingredients, name="ingredients"),
    path(
        "subscriptions/<int:author_id>",
        api.subscriptions_delete,
        name="subscribe_del",
    ),
    path("subscriptions", api.subscriptions, name="subscribe"),
    path("<username>/", views.profile, name="profile"),
    path(
        "<username>/<int:recipe_id>/edit/",
        views.recipe_edit,
        name="recipe_edit",
    ),
    path(
        "<username>/<int:recipe_id>/delete/",
        views.recipe_delete,
        name="recipe_delete",
    ),
    path("", views.index, name="index"),
]
