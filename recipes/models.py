from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=100, blank=False, verbose_name="Ingredient name"
    )
    dimension = models.CharField(max_length=100, blank=True, verbose_name="Units")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.TextField(blank=False, verbose_name="Tag name")
    colour = models.CharField(max_length=100, blank=True, verbose_name="Colour name")
    slug = models.SlugField(
        unique=True, null=True, blank=True, verbose_name="Slug name"
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    description = models.TextField(blank=False, verbose_name="Recipe description")
    name = models.CharField(max_length=100, blank=False, verbose_name="Recipe name")
    cooking_time = models.IntegerField(default=0, verbose_name="Cooking time")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        blank=False,
        verbose_name="recipe author",
    )
    image = models.ImageField(upload_to="recipes/", null=True, blank=False)
    tag = models.ManyToManyField(Tag, related_name="recipes", blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        blank=False,
        verbose_name="recipe ingredients",
    )
    is_favorite = models.BooleanField(blank=True, verbose_name="Is favorite")

    def __str__(self):
        return self.name

    def favorite_amount(self):
        return self.recipe_followers.count()

    def description_as_list(self):
        return self.description.split("\n")


class RecipeIngredient(models.Model):
    number = models.IntegerField()
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipes", blank=False
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients", blank=False
    )

    def __str__(self):
        return f"{self.ingredient.title } - {self.number} {self.ingredient.dimension}"


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="follower_recipe",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="following_recipe"
    )

    def __str__(self):
        return f"follower_recipe - {self.user} following_recipe - {self.recipe}"


class FollowUser(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"follower - {self.user} following - {self.author}"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="shoppinglist",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipes_in_shoppinglist"
    )

    def __str__(self):
        return f"user - {self.user} recipe - {self.recipe}"
