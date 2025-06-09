from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
