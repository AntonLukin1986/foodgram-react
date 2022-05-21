from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from recipes.models import Tag
from recipes.serializers import TagSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
