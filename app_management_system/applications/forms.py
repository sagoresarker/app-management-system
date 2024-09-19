from django import forms
from .models import Application, Review

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
