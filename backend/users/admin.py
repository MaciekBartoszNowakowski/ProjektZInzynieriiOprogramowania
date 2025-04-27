from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            "fields": ("role", "academic_title", "description", "updated_at")
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "academic_title", "is_active", "is_staff")
    list_filter = ("role", "academic_title", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")