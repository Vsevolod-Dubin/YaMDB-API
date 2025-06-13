from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register("titles", TitleViewSet)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("users", UserViewSet, basename="users")
router.register("auth", AuthViewSet, basename="auth")


urlpatterns = [
    path("v1/", include(router.urls)),
]
