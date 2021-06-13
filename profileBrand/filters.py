import django_filters
from django_filters import filters
from product.models import Brand

class brandFilters(django_filters.FilterSet):

    brandName = filters.CharFilter(label='Search Brand',lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ['brandName']
