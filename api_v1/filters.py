from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter()
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'description', 'name',)
