import django_filters

from cars.models import Brand, CarModel


class BrandFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ['search']


class CarModelFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    brand_id = django_filters.NumberFilter(field_name='brand_id')

    class Meta:
        model = CarModel
        fields = ['brand_id', 'search']
