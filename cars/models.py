import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

from cars.choices import CarCondition
from cars.managers import CarManager
from common.model import SoftDeleteByActiveModel


def current_year_plus_one():
    return datetime.date.today().year + 1


def validate_car_year(value):
    current_year = datetime.date.today().year
    if value < 1886 or value > current_year + 1:
        raise ValidationError(f"Year must be between 1886 and {current_year + 1}.")


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

    year = models.IntegerField(
        validators=[
            MinValueValidator(1886),
            MaxValueValidator(current_year_plus_one),
        ]
    )

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
