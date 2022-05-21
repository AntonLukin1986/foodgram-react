from rest_framework import serializers

from recipes.models import Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    color = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
