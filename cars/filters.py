import django_filters

from cars.models import Brand, Car, CarModel


class BrandFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    class Meta:
        model = Brand
        fields = ['search']


class CarModelFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    brand_id = django_filters.NumberFilter(field_name='brand_id')

    class Meta:
        model = CarModel
        fields = ['brand_id', 'search']


class CarFilter(django_filters.FilterSet):
    brand_id = django_filters.NumberFilter(
        field_name='model__brand_id',
    )
    model_id = django_filters.NumberFilter(
        field_name='model_id',
    )
    seller_id = django_filters.NumberFilter(
        field_name='seller_id',
    )

    year = django_filters.NumberFilter(
        field_name='year',
    )
    year_gte = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='gte',
    )
    year_lte = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='lte',
    )

    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
    )
    condition = django_filters.CharFilter(
        field_name='condition',
    )

    price_gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
    )
    price_lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
    )

    class Meta:
        model = Car
        fields = [
            'brand_id',
            'model_id',
            'seller_id',
            'year',
            'year_gte',
            'year_lte',
            'city',
            'condition',
            'price_gte',
            'price_lte',
        ]
