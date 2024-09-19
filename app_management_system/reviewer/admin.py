from django.contrib import admin
from .models import ReviewerAssignment

@admin.register(ReviewerAssignment)
class ReviewerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('application', 'reviewer', 'assigned_date')
    search_fields = ('application__title', 'reviewer__username')
