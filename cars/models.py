from django.db import models
from django_extensions.db.models import TimeStampedModel

class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name


class CarModel(TimeStampedModel):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_models')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'models'
        unique_together = ['brand', 'name']

    def __str__(self):
        return f"{self.brand.name} {self.name}"
