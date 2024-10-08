from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['text_field_1', 'text_field_2', 'dropdown_field_1', 'dropdown_field_2', 'image', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.Select):
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            elif not isinstance(self.fields[field].widget, forms.CheckboxSelectMultiple):
                self.fields[field].widget.attrs.update({'class': 'form-control'})