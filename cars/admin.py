from django.contrib import admin

from cars.models import Brand, CarModel


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
