from django.contrib import admin
from thesis.models import Thesis

@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ("supervisor_id", "thesis_type", "name", "max_students", "status", "language")
    search_fields = ("supervisor_id", "thesis_type", "name", "status")
    fields = ("supervisor_id", "thesis_type", "name", "description", "max_students", "status", "updated_at", "language", "tags")