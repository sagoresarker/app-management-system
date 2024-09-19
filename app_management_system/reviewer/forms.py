from django import forms
from app_management_system.applications.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
