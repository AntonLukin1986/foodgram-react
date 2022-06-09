from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет HEX', max_length=7, unique=True, null=True)
    slug = models.SlugField('Идентификатор', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'], name='unique_tag'
            )
        ]

    def __str__(self):
        return f'Название: {self.name}'


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    measurement_unit = models.CharField('Единицы измерения', max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return (
            f'Название: {self.name} ~ '
            f'Единицы измерения: {self.measurement_unit}'
        )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1, message='Не может быть меньше 1')]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'amount'],
                name='unique_ingredient_amount',
            )
        ]

    def __str__(self):
        return (
            f'Ингредиент: {self.ingredient.name} ~ '
            f'Количество: {self.amount} {self.ingredient.measurement_unit}'
        )


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    ingredients = models.ManyToManyField(
        IngredientAmount, related_name='recipes', verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    image = models.ImageField('Изображение', upload_to='recipes/images/')
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1, message='Не может быть меньше 1'),
            MaxValueValidator(1440, message='Не может быть больше 1440')
        ],
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='recipes', verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        indexes = [models.Index(fields=['name'])]
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_author_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.name} ~ автор: {self.author.first_name} '
            f'{self.author.last_name} ~ добавлен: {self.pub_date}'
        )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite_recipes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='user_favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]

    def __str__(self):
        return f'{self.user} --> {self.recipe.name}'


class CartRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='user_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
            )
        ]

    def __str__(self):
        return f'{self.user} --> {self.recipe.name}'
