from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django import forms 
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Department

from .models import AppSettings ,User
     
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
     
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First Name'
    })) 
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last Name'
    }))  
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    })) 
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    
    # groups = forms.ModelMultipleChoiceField(
    #     queryset=Group.objects.all(),
    #     required=False,
    #     widget=forms.SelectMultiple(attrs={
    #         'class': 'form-control select2',
    #     })
    # ) 
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'phone','department', 'password1', 'password2'] 
        
class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First Name'
    })) 
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last Name'
    }))  
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    })) 
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    })) 
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'multiple': 'multiple',
        })
    )
    # groups = forms.ModelMultipleChoiceField(
    #     queryset=Group.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple()
    # ) 
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'phone', 'department', 'groups']
 
class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = ["name", "favicon", "app_icon"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Application Name'}),
            }
        
class GroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Group Name'
    }))
    
    # กรอง permission ให้แยกตาม content_type
    # permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'codename'),
    #     widget=forms.SelectMultiple(attrs={
    #         'class': 'form-control select2',
    #         'multiple': 'multiple',
    #     }),
    #     required=False
    # )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    # เอา permissions ออกจาก widget, เราจะ loop ใน template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions_by_content_type = {}
        for perm in Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'codename'):
            ct = perm.content_type
            key = f"{ct.app_label}.{ct.model}"
            if key not in self.permissions_by_content_type:
                self.permissions_by_content_type[key] = []
            self.permissions_by_content_type[key].append(perm)
            
class DepartmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Department Name'
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Description', 'rows': 3
    }))
    
    class Meta:
        model = Department
        fields = ['name', 'description']         