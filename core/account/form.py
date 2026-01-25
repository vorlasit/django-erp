from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth.models import Group,Permission 
 
     
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password (leave blank to keep current password)'
    }))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar','password','groups']

    def save(self, commit=True):
        user = super().save(commit=False)

        # update simple fields
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')

        # change password
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        # avatar replace
        new_avatar = self.cleaned_data.get('avatar')
        if new_avatar:
            if user.avatar:
                user.avatar.delete(save=False)
            user.avatar = new_avatar 

        if commit:
            user.save()

            # M2M needs to save after user.save()
            self.save_m2m()

            # Save groups
            user.groups.set(self.cleaned_data['groups'])
 
           

        return user

    def __init__(self, *args, **kwargs): 
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs) 
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            self.fields['groups'].queryset = Group.objects.exclude(name__iexact='Administrator')
        else:
            self.fields['groups'].queryset = Group.objects.all()
        
        # Build permission groups
        self.permissions_by_ct = {}
        user_perms = set()
        if self.instance.pk:
            user_perms = set(self.instance.user_permissions.values_list('id', flat=True))

        for perm in Permission.objects.select_related('content_type').order_by('content_type__app_label', 'content_type__model'):
            ct = perm.content_type
            key = f"{ct.app_label}.{ct.model}"
            self.permissions_by_ct.setdefault(key, {'ct': ct, 'permissions': []})
            # Mark if user already has this permission
            self.permissions_by_ct[key]['permissions'].append({
                'id': perm.id,
                'name': perm.name,
                'checked': perm.id in user_perms,
            })

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    ) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar', 'password1', 'password2','groups' ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.avatar = self.cleaned_data.get('avatar')   
        if commit:
            user.save() 
            # ✅ Get selected groups
            selected_groups = self.cleaned_data.get('groups')

            if selected_groups:
                user.groups.set(selected_groups)
            else: 
                default_group, created = Group.objects.get_or_create(name='User')
                user.groups.add(default_group)
        return user
    def __init__(self, *args, **kwargs):
        # accept optional `user` kwarg so we can filter group choices
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Fetch all permissions grouped by content_type
        self.permissions_by_ct = {}
        for perm in Permission.objects.select_related('content_type').order_by('content_type__app_label', 'content_type__model'):
            ct = perm.content_type
            key = f"{ct.app_label}.{ct.model}"
            self.permissions_by_ct.setdefault(key, {'ct': ct, 'permissions': []})
            self.permissions_by_ct[key]['permissions'].append(perm)
        all_groups = Group.objects.all().order_by('id')

        # ✅ ถ้า user ไม่มีสิทธิ์ Administrator -> ซ่อนกลุ่มแรก
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            if all_groups.exists():
                all_groups = all_groups[1:]

        self.fields['groups'].queryset = all_groups

        # ✅ ตั้งค่า default group = "Customer" ถ้ามี
        default_group = Group.objects.filter(name__iexact="Customer")
        if default_group.exists():
            self.fields['groups'].initial = default_group
            
class RegisterNoneLogForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    })) 
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Phone'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.avatar = self.cleaned_data.get('avatar')   

        if commit:
            user.save() 
            selected_groups = self.cleaned_data.get('groups')

            if selected_groups:
                user.groups.set(selected_groups)
            else: 
                default_group, created = Group.objects.get_or_create(name='User')
                user.groups.add(default_group)  # ✅ correct usage
        return user      
    
class GroupSelectForm(forms.ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = CustomUser
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user or not user.groups.filter(name__iexact='Administrator').exists():
            self.fields['groups'].queryset = Group.objects.exclude(name__iexact='Administrator')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            group_obj = self.cleaned_data.get('groups')
            if group_obj:
                user.groups.set([group_obj])  # ✅ wrap single Group in list
        return user
    


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('content_type__app_label', 'codename'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions",
    ) 
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Group Name'
    }))

    class Meta:
        model = Group
        fields = ['name', 'permissions']  # name + permissions

    def __init__(self, *args, **kwargs):
        # accept optional `user` kwarg so we can filter group choices
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Group permissions by Content Type
        permissions = Permission.objects.select_related('content_type').all()
        group_permissions = self.instance.permissions.all() if self.instance.pk else []
        permissions_by_ct = {}

        for perm in permissions:
            ct = perm.content_type
            if ct.id not in permissions_by_ct:
                permissions_by_ct[ct.id] = {
                    'ct': ct,
                    'permissions': []
                }
            permissions_by_ct[ct.id]['permissions'].append({
                'id': perm.id,
                'name': perm.name,
                'checked': perm in group_permissions
            })

        # store for template use
        self.permissions_by_ct = permissions_by_ct