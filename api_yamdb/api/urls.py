from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register(r"titles", TitleViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"users", UserViewSet, basename="users")
router.register(r"auth", AuthViewSet, basename="auth")


urlpatterns = [
    path("", include(router.urls)),
]
