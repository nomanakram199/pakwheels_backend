from cars.models import Car


class CarQuerysetMixin:
    def get_base_queryset(self):
        return (
            Car.objects.filter(is_deleted=False)
            .select_related('model__brand', 'seller')
            .prefetch_related('images')
        )

