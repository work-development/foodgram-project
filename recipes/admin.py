from django.contrib import admin

from .models import (FollowRecipe, FollowUser, Ingredient, Recipe,
                     RecipeIngredient, ShoppingList, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("description", "cooking_time", "pub_date", "author", "image", "name", "is_favorite")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("description",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)

# при регистрации модели Recipe источником конфигурации для неё назначаем класс RecipeAdmin
admin.site.register(Recipe, RecipeAdmin)

class TagAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("name", "colour", "slug")


admin.site.register(Tag, TagAdmin)

class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ("title", "dimension")
    search_fields = ("title",)

admin.site.register(Ingredient, IngredientAdmin)

class FollowRecipeAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("user", "recipe")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("user",)

admin.site.register(FollowRecipe, FollowRecipeAdmin)

admin.site.register(FollowUser)
admin.site.register(ShoppingList)
admin.site.register(RecipeIngredient)



