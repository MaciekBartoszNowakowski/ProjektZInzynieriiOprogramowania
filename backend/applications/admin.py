from django.contrib import admin
from applications.models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'thesis', 'status']
    list_filter = ['thesis__thesis_type', 'thesis__status']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name', 'thesis__name']
