from django.db.models import expressions, query
import django_filters
from product.models import Product, Brand

class productFilters(django_filters.FilterSet):

    CHOICE = [
        ('avgScore', 'avgScore'),
        ('dateTime', 'dateTime')
    ]

    ordering = django_filters.ChoiceFilter(label='ordering', choices=CHOICE, method='filter_by_order')

    def filter_by_order (self,queryset,name,value):
        expression = '-avgScore' if value == 'avgScore' else '-dtm_crt'
        return queryset.order_by(expression)
    
    class Meta:
        model = Product
        fields = {
            'productName':['icontains'],
            'brandId__brandName':['icontains'],
            'categoryId__categoryName':['icontains']
        }



