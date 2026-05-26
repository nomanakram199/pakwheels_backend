from django.contrib import admin

from cars.models import Brand, CarModel, Car, Image


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created', 'modified']
    search_fields = ['name']
    readonly_fields = ['created', 'modified']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'created', 'modified']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']
    readonly_fields = ['created', 'modified']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'seller', 'year', 'license_plate', 'city', 'price', 'condition', 'is_deleted', 'created', 'modified']
    list_filter = ['model', 'seller', 'city', 'condition', 'is_deleted']
    search_fields = ['model__name', 'seller__username', 'license_plate', 'city']
    readonly_fields = ['created', 'modified']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'image', 'is_primary', 'display_order', 'created', 'modified']
    list_filter = ['car', 'is_primary']
    search_fields = ['car__model__name', 'car__license_plate']
    readonly_fields = ['created', 'modified']
