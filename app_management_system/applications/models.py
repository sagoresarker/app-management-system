from django.db import models
from django.conf import settings

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    text_field_1 = models.TextField()
    text_field_2 = models.TextField()
    dropdown_field_1 = models.CharField(max_length=100, choices=[('Option1', 'Option 1'), ('Option2', 'Option 2')])
    dropdown_field_2 = models.CharField(max_length=100, choices=[('OptionA', 'Option A'), ('OptionB', 'Option B')])
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Application by {self.user.username} - {self.id}"