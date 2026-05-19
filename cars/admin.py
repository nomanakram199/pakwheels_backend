from django.contrib import admin
from cars.models import Brand, CarModel


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'created_at']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'created_at']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']
