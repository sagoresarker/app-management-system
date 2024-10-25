from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new users
            if obj.role in ['admin', 'reviewer']:
                password = CustomUser.generate_random_password()
                obj.set_password(password)
                self.send_credentials_email(obj, password)
        super().save_model(request, obj, form, change)

    def send_credentials_email(self, user, password):
        subject = 'Your Account Credentials'
        html_message = render_to_string('core/credentials_email.html', {
            'user': user,
            'password': password,
        })
        plain_message = strip_tags(html_message)
        from_email = 'noreply@yourdomain.com'
        send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

admin.site.register(CustomUser, CustomUserAdmin)

# Change the site header and title
admin.site.site_header = "Application Management System"
admin.site.site_title = "Application Management System"
admin.site.index_title = "Welcome to Application Management"
