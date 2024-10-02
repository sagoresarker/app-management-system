from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_field_1', 'dropdown_field_1', 'image', 'file')  # Adjust according to your model fields
    search_fields = ('user__username', 'text_field_1', 'dropdown_field_1')  # Adjust according to your model fields

