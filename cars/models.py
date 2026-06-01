from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from cars.choices import CarCondition
from cars.managers import CarManager
from cars.validators import validate_car_year
from core.model import SoftDeleteByActiveModel


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


class Car(SoftDeleteByActiveModel, TimeStampedModel):
    objects = CarManager()
    all_objects = models.Manager()

    model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name='cars',
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars',
    )

    year = models.IntegerField(validators=[validate_car_year])
    license_plate = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CarCondition.choices)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'cars'
        indexes = [
            models.Index(fields=['seller_id']),
            models.Index(fields=['is_active']),
            models.Index(fields=['model_id']),
        ]

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.license_plate}"


class Image(TimeStampedModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/images/')
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'images'
        indexes = [
            models.Index(fields=['car_id']),
        ]

    def __str__(self):
        return f"Image for {self.car.license_plate}"
