from django.db import models
from django.contrib.auth.models import User
from app_management_system.applications.models import Application
from django.conf import settings

class ReviewerAssignment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewer {self.reviewer.username} assigned to {self.application.title}"
