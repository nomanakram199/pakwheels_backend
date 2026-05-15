from django.db import models

# Create your models here.
from django.db import models
from catalog.models import Model
from users.models import User
from cars.choices import CONDITION_CHOICES

 
class Car(models.Model):
    model = models.ForeignKey(Model, on_delete=models.PROTECT, related_name='cars')
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cars'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.model} - {self.license_plate}"


