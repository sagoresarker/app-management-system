from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)



# Change the site header and title
admin.site.site_header = "Application Management System"
admin.site.site_title = "Application Management System"
admin.site.index_title = "Welcome to Application Management"
