from django.contrib import admin
from django.urls import include, path
from recipes.views import TagViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('tags/<int:tag_id>/', TagViewSet, basename='tag')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls))
]
