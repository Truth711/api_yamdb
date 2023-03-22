from django_filters import FilterSet, CharFilter
from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='iexact')
    category = CharFilter(field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category',)
