# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
        ('reviewer', 'Reviewer'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    email = models.EmailField(unique=True)

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def is_reviewer(self):
        return self.role == 'reviewer'

    @staticmethod
    def generate_random_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))