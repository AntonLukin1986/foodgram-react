from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, allow_blank=False)
    color = serializers.CharField(max_length=7, allow_blank=False)
    slug = serializers.SlugField(
        max_length=200,
        allow_blank=False,
        validators=[UniqueValidator(queryset=Tag.objects.all())]
    )

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
