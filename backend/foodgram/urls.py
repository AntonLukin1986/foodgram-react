from django.contrib import admin
from django.urls import include, path
from recipes.views import IngredientViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('tags/<int:tag_id>/', TagViewSet, basename='tag')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('ingredients/<int:ingred_id>/', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(router_v1.urls))
]
