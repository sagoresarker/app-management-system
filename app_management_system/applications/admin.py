from django.contrib import admin
from .models import Application, Review

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'submission_date')
    search_fields = ('title', 'user__username', 'status')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'reviewer', 'review_date')
    search_fields = ('application__title', 'reviewer__username')
