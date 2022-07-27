import datetime as dt

from django.test import TestCase

from recipes.models import (
    Tag, Ingredient, IngredientAmount, Recipe, FavoriteRecipe, CartRecipe
)
from users.models import User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='Автор', first_name='Ан', last_name='Лу',
            email='mail@mail.ru'
        )
        cls.tag = Tag.objects.create(name='Тэг', color='#000000', slug='slug')
        cls.ingredient = Ingredient.objects.create(
            name='Фасоль', measurement_unit='г.'
        )
        cls.amount = IngredientAmount.objects.create(
            ingredient=cls.ingredient, amount=10
        )
        cls.recipe = Recipe.objects.create(
            name='Рецепт',
            text='Описание рецепта',
            cooking_time=10,
            author=cls.author
        )
        cls.recipe.ingredients.set([cls.ingredient.id]),
        cls.recipe.tags.set([cls.tag.id]),
        cls.fav_recipe = FavoriteRecipe.objects.create(
            user=cls.author, recipe=cls.recipe
        )
        cls.cart = CartRecipe.objects.create(
            user=cls.author, recipe=cls.recipe
        )

    def test_models_have_correct_object_names(self):
        """Проверка корректной работы метода __str__ у моделей."""
        models_expected = {
            self.tag: 'Название: Тэг',
            self.ingredient: 'Название: Фасоль ~ Единицы измерения: г.',
            self.amount: 'Ингредиент: Фасоль ~ Количество: 10 г.',
            self.recipe: f'Рецепт ~ автор: Ан Лу ~ добавлен: '
                         f'{dt.date.today().strftime("%d.%m.%Y")}',
            self.fav_recipe: 'Автор <mail@mail.ru> --> Рецепт',
            self.cart: 'Автор <mail@mail.ru> --> Рецепт'
        }
        for model, expected in models_expected.items():
            with self.subTest(field=model):
                self.assertEqual(str(model), expected)
