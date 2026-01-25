from django import forms
from .models import AppSettings 

 
class AppSettingsForm(forms.ModelForm):

    class Meta:
        model = AppSettings
        fields = ["name", "favicon", "app_icon"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application Name'}),
            }
     