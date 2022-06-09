from django.contrib import admin

from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientAmount, Recipe, Tag)

admin.site.register(Tag)
admin.site.register(IngredientAmount)
admin.site.register(FavoriteRecipe)
admin.site.register(CartRecipe)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-----'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'in_favorites', 'ingredients_amount')
    list_filter = ('name', 'tags', 'author')
    search_fields = ('name', 'author__username',)
    empty_value_display = '-----'

    @admin.display(description='В избранных')
    def in_favorites(self, obj):
        return obj.user_favorites.count()

    @admin.display(description='Ингредиентов')
    def ingredients_amount(self, obj):
        return obj.ingredients.count()
