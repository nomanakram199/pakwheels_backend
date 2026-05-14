from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'city', 'is_verified', 'is_staff']
    search_fields = ['email',]
    readonly_fields = ('created_at', 'updated_at')

