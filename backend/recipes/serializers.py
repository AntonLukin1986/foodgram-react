import base64
import uuid

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CustomUserSerializer

from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientAmount, Recipe, Tag)

MIN_AMOUNT = 'Количество не может быть меньше 1'


class Base64ToImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            service, image = data.split(';base64,')
            extention = service.split('/')[-1]
            id_ = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(image), name=id_.urn[9:] + '.' + extention
            )
        return super().to_internal_value(data)


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
                message='Вы уже создавали рецепт с таким названием!'
            )
        ]

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
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        ingredients_amounts = self.create_ingredients_amounts(ingredients)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.ingredients.set(ingredients_amounts)
        return recipe

    def update(self, instance, validated_data):
        ingredients_amounts = self.create_ingredients_amounts(
            validated_data.get('ingredients')
        )
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        instance.tags.set(validated_data.get('tags'))
        instance.ingredients.clear()
        instance.ingredients.set(ingredients_amounts)
        instance.save()
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
