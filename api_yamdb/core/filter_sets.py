import django_filters
from django_filters import rest_framework

from reviews.models import Title


class TitlesFilterSet(rest_framework.FilterSet):
    """Зададим фильтрсет для вьюсета TitlesAPI"""
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
