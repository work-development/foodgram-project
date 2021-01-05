from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .utils import*
from .constants import*
from .models import (FollowRecipe, FollowUser, Ingredient, Recipe,
                     RecipeIngredient, ShoppingList, Tag, User)


def index(request):
    print(request.GET)
    slugs = request.GET.getlist("filters")
    if slugs != []:
        recipe_list = Recipe.objects.order_by("-pub_date").filter(tag__slug__in=slugs)
    else:
        recipe_list = Recipe.objects.order_by("-pub_date").all()
    paginator = Paginator(recipe_list, ITEMS_PER_PAGE)
    page_number = request.GET.get(
        "page"
    )
    page = paginator.get_page(page_number)  
    favorites_list = []
    if request.user.is_authenticated and not request.user.is_anonymous:
        l = (
            ShoppingList.objects.filter(user=request.user)
            .select_related("recipe")
            .values_list("recipe_id", flat=True)
        )
        shopping_list = Recipe.objects.filter(id__in=l).values_list("id", flat=True)
        return render(
            request,
            "indexAuth.html",
            {
                "page": page,
                "paginator": paginator,
                "shopping_list": shopping_list,
                "favorites_list": favorites_list,
                "all_tags": Tag.objects.all(),
            },
        )
    return render(
        request,
        "indexAuth.html",
        {
            "page": page,
            "paginator": paginator,
            "all_tags": Tag.objects.all(),
            "favorites_list": favorites_list,
        },
    )


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.recipe_ingredients.all()
    is_author = False
    if request.user.is_authenticated:
        subscriptions_list = FollowUser.objects.filter(user=request.user).values_list(
            "author", flat=True
        )
        shopping_list = ShoppingList.objects.filter(user=request.user).values_list(
            "id", flat=True
        )
        is_author = True
        return render(
            request,
            "singlePage.html",
            {
                "recipe": recipe,
                "is_author": is_author,
                "ingredients": ingredients,
                "subscriptions_list": subscriptions_list,
                "shopping_list": shopping_list,
                "user": request.user,
            },
        )
    return render(
        request,
        "singlePage.html",
        {"recipe": recipe, "is_author": is_author, "ingredients": ingredients},
    )


def profile(request, username):
    all_tags = Tag.objects.all()
    if username == "admin_recipes":
        username = "admin"
    author_profile = get_object_or_404(User, username=username)
    tags = Tag.objects.filter(slug__in=request.GET.getlist("filters")).values_list(
        "name", flat=True
    )
    tags = list(set(tags))
    if tags != []:
        t = (
            Tag.objects.filter(name__in=tags)
            .select_related("recipes")
            .values_list("recipes", flat=True)
        )
        recipe_list = (
            Recipe.objects.order_by("-pub_date")
            .filter(id__in=t)
            .filter(author=author_profile)
        )
    else:
        recipe_list = Recipe.objects.order_by("-pub_date").filter(author=author_profile)
    paginator = Paginator(recipe_list, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    following = False
    my_profile = False
    if request.user.is_authenticated:
        following = FollowUser.objects.filter(user=request.user).filter(
            author=author_profile
        )
        my_profile = request.user
    return render(
        request,
        "authorRecipe.html",
        {
            "recipes": recipe_list,
            "username": username,
            "author_profile": author_profile,
            "page": page,
            "paginator": paginator,
            "following": following,
            "my_profile": my_profile,
            "all_tags": all_tags,
        },
    )


@login_required
def new_recipe(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            tags = get_tags(request)
            author_ingredients, values = add_ingredients(request)
            text = request.POST["description"]
            form = RecipeForm(request.POST or None, files=request.FILES or None)

            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.is_favorite = False
                recipe.author = request.user
                recipe.save()
                for tag in tags:
                    recipe.tag.add(tag)
                recipe.name = request.POST["name"]
                recipe.cooking_time = request.POST["cooking_time"]
                recipe.save()
                for i, ingredient in enumerate(author_ingredients):
                    recipe_ingredient = RecipeIngredient(
                        number=values[i], ingredient=ingredient.get(), recipe=recipe
                    )
                    recipe_ingredient.save()

                recipe.description = text
                form.save_m2m()
                return redirect("/")
        form = RecipeForm()
        ingredients_list = Ingredient.objects.all()
        return render(
            request,
            "formRecipe.html",
            {
                "form": form,
                "a": [request.POST, request.POST.getlist("name")],
                "ingredients_list": ingredients_list,
            },
        )
    return redirect("index")


@login_required
def subscribe_list(request):
    list_of_authors_I_follow = FollowUser.objects.filter(user=request.user)
    paginator = Paginator(list_of_authors_I_follow, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "myFollow.html", {"page": page, "paginator": paginator})


@login_required
def favorites_page(request):
    all_tags = Tag.objects.all()
    tags = Tag.objects.filter(slug__in=request.GET.getlist("filters")).values_list(
        "name", flat=True
    )
    tags = list(set(tags))
    favorites_list = (
        FollowRecipe.objects.filter(user=request.user)
        .select_related("recipe")
        .values_list("recipe_id", flat=True)
    )
    if tags != []:
        t = (
            Tag.objects.filter(name__in=tags)
            .select_related("recipes")
            .values_list("recipes", flat=True)
        )
        recipe_list = (
            Recipe.objects.order_by("-pub_date")
            .filter(id__in=t)
            .filter(id__in=favorites_list)
        )
    else:
        recipe_list = Recipe.objects.order_by("-pub_date").filter(id__in=favorites_list)

    paginator = Paginator(recipe_list, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    l = (
        ShoppingList.objects.filter(user=request.user)
        .select_related("recipe")
        .values_list("recipe_id", flat=True)
    )
    shopping_list = Recipe.objects.filter(id__in=l).values_list("id", flat=True)

    return render(
        request,
        "favorite.html",
        {
            "page": page,
            "paginator": paginator,
            "shopping_list": shopping_list,
            "favorites_list": favorites_list,
            "all_tags": all_tags,
        },
    )


def shop_list(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        shopping_list = (
            ShoppingList.objects.filter(user=user)
            .select_related("recipe")
            .values_list("recipe_id", flat=True)
        )
        recipe_shopping_list = Recipe.objects.filter(id__in=shopping_list)
        paginator = Paginator(recipe_shopping_list, ITEMS_PER_PAGE)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)
        return render(request, "shopList.html", {"page": page, "paginator": paginator})
    else:
        return redirect("/auth/login/")


@login_required
def delete_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = get_object_or_404(User, username=request.user.username)
    purchase = get_object_or_404(ShoppingList, user=user, recipe=recipe)
    purchase.delete()
    return redirect("shop_list")


def download_shopping_list(request):
    recipes = Recipe.objects.filter(recipes_in_shoppinglist__user=request.user)
    ingredients = recipes.values(
        "ingredients__title", "ingredients__dimension"
    ).annotate(total_amount=Sum("recipe_ingredients__number"))
    file_data = ""
    for item in ingredients:
        line = " ".join(str(value) for value in item.values())
        file_data += line + "\n"
    response = HttpResponse(file_data, content_type="application/text charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="ShoppingList.txt"'
    return response


@login_required
def recipe_edit(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=profile)
    tag_name = (
        Recipe.objects.filter(pk=recipe_id, author=profile)
        .select_related("recipes")
        .values_list("tag__slug", flat=True)
    )
    if request.user != profile:
        return redirect("recipe_page", recipe_id=recipe_id)
    ingredients = recipe.ingredients.through.objects.filter(recipe=recipe).all()
    tags = get_tags(request)

    author_ingredients, values = add_ingredients(request)


    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    if request.method == "POST":
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.tag.clear()
            for tag in tags:
                recipe.tag.add(tag)
            recipe.save()
            for i, ingredient in enumerate(author_ingredients):
                recipe_ingredient = RecipeIngredient(
                    number=values[i], ingredient=ingredient.get(), recipe=recipe
                )
                recipe_ingredient.save()

            form.save_m2m()
            return redirect("recipe_page", recipe_id=recipe_id)

    return render(
        request,
        "formChangeRecipe.html",
        {
            "form": form,
            "recipe": recipe,
            "tag_name": tag_name,
            "ingredients": ingredients,
        },
    )


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.username == username:
        recipe.delete()
        return redirect("/")


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
