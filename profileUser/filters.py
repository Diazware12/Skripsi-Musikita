import django_filters
from django_filters import filters
from register.models import User

class userFilters(django_filters.FilterSet):

    userName = filters.CharFilter(label='Search Name',lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['userName']
