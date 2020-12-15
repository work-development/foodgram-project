from django.urls import path

from . import views

urlpatterns = [
    path("recipe/<int:recipe_id>/", views.RecipeDetailView, name="recipe_page"),
    path("favorites", views.add_favorites, name="favorite_add"),
    path(
        "favorites/<int:favorite_id>/", views.delete_favorites, name="favorite_delete"
    ),
    path("new_recipe", views.new_recipe, name="new_recipe"),
    path("subscribe_list", views.subscribe_list, name="subscribe_list"),
    path("favorites_page", views.favorites_page, name="favorites_page"),
    path(
        "shop_list/dowload/",
        views.download_shopping_list,
        name="download_shopping_list",
    ),
    path("shop_list/<int:recipe_id>/", views.delete_purchase, name="delete_purchase"),
    path("shop_list", views.shop_list, name="shop_list"),
    path("purchases/<int:id>", views.purchases_delete, name="purchases_del"),
    path("purchases", views.purchases, name="purchases"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path(
        "subscriptions/<int:author_id>",
        views.subscriptions_delete,
        name="subscribe_del",
    ),
    path("subscriptions", views.subscriptions, name="subscribe"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:recipe_id>/edit/", views.recipe_edit, name="recipe_edit"),
    path(
        "<username>/<int:recipe_id>/delete/", views.recipe_delete, name="recipe_delete"
    ),
    path("", views.index, name="index"),
]
