import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        "category__slug",
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        "genre__slug",
        lookup_expr='exact'
    )
    name = django_filters.CharFilter(
        "name",
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year',)
