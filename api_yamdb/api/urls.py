from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
