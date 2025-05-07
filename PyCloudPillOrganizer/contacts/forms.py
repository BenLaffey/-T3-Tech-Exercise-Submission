from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['id', 'medication_name', 'administration_notes', 'usage_time', 'usage_importance']
        # Apply CSS styles
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter medication name',
            }),
            'administration_notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter administration notes',
                }),
	    'usage_time': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter usage time',
            }),
            'usage_importance': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter usage importance',
            }),
        }
