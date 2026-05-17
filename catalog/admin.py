from django.contrib import admin
from catalog.models import Brand, Model


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'created_at']
    search_fields = ['name']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'created_at']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']


