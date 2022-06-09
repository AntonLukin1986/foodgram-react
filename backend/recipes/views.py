from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import RecipeInfoSerializer

from recipes.file_download import download_pdf, download_txt
from recipes.filters import RecipeFilter
from recipes.models import (CartRecipe, FavoriteRecipe, Ingredient,
                            IngredientAmount, Recipe, Tag)
from recipes.permissions import IsAuthorOrReadOnly
from recipes.serializers import (IngredientSerializer, RecipeReadSerializer,
                                 RecipeSerializer, TagSerializer)

IN_FAVORITE_ERROR = {'errors': 'Рецепт уже добавлен в избранные!'}
NOT_IN_FAVORITE_ERROR = {'errors': 'Рецепта нет в избранных!'}
IN_CART_ERROR = {'errors': 'Рецепт уже добавлен в список покупок!'}
NOT_IN_CART_ERROR = {'errors': 'Рецепта нет в списке покупок!'}


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('@name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            name='download_cart')
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipes__user_carts__user=request.user
            ).order_by(
                'ingredient__name'
            ).annotate(
                total=Sum('amount')
            ).values(
                'ingredient__name', 'total', 'ingredient__measurement_unit'
            )
        if not ingredients:
            return Response(status=status.HTTP_404_NOT_FOUND)
        to_buy = {
            item['ingredient__name']:
            [item['total'], item['ingredient__measurement_unit']]
            for item in ingredients
        }
        file_format = list(request.query_params.keys())[0]
        if file_format == 'pdf':
            return download_pdf(to_buy, HttpResponse, pdfmetrics,
                                TTFont, Canvas, Recipe, request)
        return download_txt(to_buy, Recipe, request, HttpResponse, status)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,),
            name='favorite')
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            _, created = FavoriteRecipe.objects.get_or_create(
                recipe=recipe, user=request.user
            )
            if created:
                return Response(
                    RecipeInfoSerializer(recipe).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                IN_FAVORITE_ERROR, status=status.HTTP_400_BAD_REQUEST
            )

        favorite_recipe = FavoriteRecipe.objects.filter(
            recipe=recipe, user=request.user
        )
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            NOT_IN_FAVORITE_ERROR, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,),
            name='shopping_cart')
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            _, created = CartRecipe.objects.get_or_create(
                recipe=recipe, user=request.user
            )
            if created:
                return Response(
                    RecipeInfoSerializer(recipe).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(IN_CART_ERROR, status=status.HTTP_400_BAD_REQUEST)
        cart_recipe = CartRecipe.objects.filter(
            recipe=recipe, user=request.user
        )
        if cart_recipe.exists():
            cart_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(NOT_IN_CART_ERROR, status=status.HTTP_400_BAD_REQUEST)
