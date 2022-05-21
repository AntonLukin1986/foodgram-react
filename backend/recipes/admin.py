from django.contrib import admin

from recipes.models import Ingredient, Tag  # Recipe,

admin.site.register(Tag)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_filter = ('name', 'tags')  # user
