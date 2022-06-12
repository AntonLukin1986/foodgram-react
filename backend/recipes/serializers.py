from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.fields import Base64ToImageField
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientAmount, Recipe, Tag)
from users.serializers import CustomUserSerializer

MIN_AMOUNT = {'amount': 'Количество не может быть меньше 1'}
RECIPE_DUPLICATE_ERROR = 'Вы уже создавали рецепт с таким названием!'
TAGS_DUPLICATE_ERROR = {'tags': 'Тэги не должны дублироваться!'}
INGREDIENTS_DUPLICATE_ERROR = {
    'ingredients': 'Ингредиенты не должны дублироваться!'
}


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(MIN_AMOUNT)
        return value


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ToImageField()
    cooking_time = serializers.IntegerField(min_value=1, max_value=1440)
    author = CustomUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'tags', 'image', 'text',
                  'cooking_time', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name', 'author'),
                message=RECIPE_DUPLICATE_ERROR
            )
        ]

    def validate(self, data):
        tags = data['tags']
        if len(tags) > len(set(tags)):
            raise serializers.ValidationError(TAGS_DUPLICATE_ERROR)
        ingredients_id = [
            ingredient['ingredient']['id'] for ingredient
            in data['ingredients']
        ]
        if len(ingredients_id) > len(set(ingredients_id)):
            raise serializers.ValidationError(INGREDIENTS_DUPLICATE_ERROR)
        return data

    def create_ingredients_amounts(self, ingredients):
        ingredients_amounts = []
        for ingredient in ingredients:
            ingredient_amount, _ = IngredientAmount.objects.get_or_create(
                ingredient=get_object_or_404(
                    Ingredient, id=ingredient['ingredient']['id']
                ),
                amount=ingredient['amount']
            )
            ingredients_amounts.append(ingredient_amount)
        return ingredients_amounts

    def create(self, validated_data):
        ingredients_amounts = self.create_ingredients_amounts(
            validated_data.pop('ingredients')
        )
        recipe = super().create(validated_data)
        recipe.ingredients.set(ingredients_amounts)
        return recipe

    def update(self, instance, validated_data):
        ingredients_amounts = self.create_ingredients_amounts(
            validated_data.pop('ingredients')
        )
        instance = super().update(instance, validated_data)
        instance.ingredients.set(ingredients_amounts)
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'tags', 'image', 'text',
                  'cooking_time', 'author', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return CartRecipe.objects.filter(user=user, recipe=obj).exists()
