# /api_yamdb/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, AuthViewSet
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserViewSet, basename='users')
router.register(r'auth', AuthViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
]
