from .models import Tag, Ingredient

def get_tags(request):
    tagss = []
    for tag in ["breakfast", "lunch", "dinner"]:
        if tag in request.POST.dict().keys():
            tagss.append(tag)

    tags = Tag.objects.filter(slug__in=tagss)
    return tags


def add_ingredients(request):
    author_ingredients = []
    values = []
    for key in request.POST.keys():
        if key.split("_")[0] == "nameIngredient":
            author_ingredients.append(
                Ingredient.objects.filter(title=request.POST[key])
            )
        if key.split("_")[0] == "valueIngredient":
            values.append(request.POST[key])

    return author_ingredients, values





