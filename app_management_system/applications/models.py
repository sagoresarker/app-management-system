from django.db import models
from django.contrib.auth import get_user_model

class Application(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text_field_1 = models.TextField()
    text_field_2 = models.TextField()
    dropdown_field_1 = models.CharField(max_length=100, choices=[('Option1', 'Option 1'), ('Option2', 'Option 2')])
    dropdown_field_2 = models.CharField(max_length=100, choices=[('OptionA', 'Option A'), ('OptionB', 'Option B')])
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    checklist = models.ManyToManyField('ChecklistItem')

    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.user.username} - {self.id}"

class ChecklistItem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
