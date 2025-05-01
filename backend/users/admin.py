from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, AcademicTitle, StudentProfile, SupervisorProfile, Logs

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Custom Fields", {
            "fields": (
                "role",
                "academic_title",
                "description",
                "department",
                "tags",
                "updated_at",
            ),
        }),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "academic_title",
        "department",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    )

    list_filter = (
        "role",
        "academic_title",
        "department",
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "department__name",
    )
    ordering = ("-date_joined",)

    date_hierarchy = "date_joined"

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "index_number")
    search_fields = ("user__username", "user__first_name", "user__last_name", "index_number")
    fields = ("user", "index_number")

@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bacherol_limit",
        "engineering_limit",
        "master_limit",
        "phd_limit",
    )
    search_fields = ("user__username", "user__first_name", "user__last_name")
    fields = (
        "user",
        "bacherol_limit",
        "engineering_limit",
        "master_limit",
        "phd_limit",
    )

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "timestamp", "description_snippet")
    list_filter = ("timestamp", "user_id")
    search_fields = ("user_id__username", "description")
    fields = ("user_id", "timestamp", "description")

    def description_snippet(self, obj):
        return obj.description[:100] + '...' if obj.description and len(obj.description) > 100 else obj.description
    description_snippet.short_description = "Description"