from django import forms
from .models import Request
from base.models import User

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'type', 'description', 'department', 'request_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 4}),
            'department': forms.Select(attrs={'class': 'form-control'}), # Cleaned up
            'request_to': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        if 'department' in self.data:
            dept_id = int(self.data.get('department'))
            self.fields['request_to'].queryset = User.objects.filter(department_id=dept_id) 
        elif self.instance.pk:
            self.fields['request_to'].queryset = User.objects.filter(department=self.instance.department)
        else:
            self.fields['request_to'].queryset = User.objects.none() 