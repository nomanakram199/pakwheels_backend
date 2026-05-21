from django.contrib import admin

from users.models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'is_verified', 'is_staff', 'created', 'modified']
    search_fields = ['email', 'phone_number']
    readonly_fields = ['created', 'modified']
