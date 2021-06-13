import django_filters
from django_filters import filters
from product.models import Category, Product, Brand

class productFilters(django_filters.FilterSet):

    CHOICE = [
        ('avgScore', 'avgScore'),
        ('dateTime', 'dateTime')
    ]

    ordering = django_filters.ChoiceFilter(label='ordering', choices=CHOICE, method='filter_by_order')

    def filter_by_order (self,queryset,name,value):
        expression = '-avgScore' if value == 'avgScore' else '-dtm_crt'
        return queryset.order_by(expression)
    
    brandList = Brand.objects.all()
    brand_choice = [[obj.brandId,obj.brandName] for obj in brandList]
    categoryList = Category.objects.all()
    category_choice = [[obj.categoryId,obj.categoryName] for obj in categoryList]

    productName = filters.CharFilter(label='Product Name',lookup_expr='icontains')
    brandId = filters.ChoiceFilter(label='Brand Name',choices=brand_choice)
    categoryId = filters.ChoiceFilter(label='Category',choices=category_choice)

    class Meta:
        model = Product
        fields = ['productName','brandId','categoryId']
