from django.urls import include, path
<<<<<<< HEAD

from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, UserViewSet

=======
from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, UserViewSet
>>>>>>> origin/develop

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"auth", AuthViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
]
