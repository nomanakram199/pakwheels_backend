from django.db import models


class CarQuerySet(models.QuerySet):
    def car_relations_query(self):
        return (
            self.select_related('model__brand', 'seller')
            .prefetch_related('images')
        )


class CarManager(models.Manager.from_queryset(CarQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
