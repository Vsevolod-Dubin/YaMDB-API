from api.permissions import IsAdminOrReadOnly
from rest_framework import filters, mixins, viewsets


class GroupBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
