from django.contrib import admin
from cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'model', 'year', 'price', 'seller', 'condition', 'is_deleted', 'created_at']
    list_filter = ['condition', 'is_deleted', 'created_at']
    search_fields = ['license_plate', 'model__name', 'seller__email']
    readonly_fields = ['created_at', 'updated_at']


