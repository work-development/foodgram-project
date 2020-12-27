from django import forms

from .models import Ingredient, Recipe, Tag


class RecipeForm(forms.ModelForm):
    #tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), to_field_name="slug")
    #ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), to_field_name='title')
    #number = []
    class Meta:
            model = Recipe
            fields = ["name", "cooking_time", "description", "image"]



