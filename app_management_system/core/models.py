from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
        ('reviewer', 'Reviewer'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def is_reviewer(self):
        return self.role == 'reviewer'

