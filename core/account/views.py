from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import Group
from .form import (RegisterForm,EditUserForm ,GroupForm) 
# Create your views here.
from .models import CustomUser
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout 
from django.contrib.auth.models import Permission 
@login_required
def profile(request):
    users = CustomUser.objects.all()
    return render(request, 'profile.html', {'users': users}) 

def register_view(request): 
    user = request.user
    if request.method == 'POST': 
        form = RegisterForm(request.POST, request.FILES, user=user)        
        if form.is_valid():
            user = form.save()
            perm_ids = request.POST.getlist('permissions')
            user.user_permissions.set(Permission.objects.filter(id__in=perm_ids))
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm(user=user)
    return render(request, 'register.html', {'form': form })

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user, user=request.user)
        if form.is_valid():
            
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            form.save()

            # Update user permissions
            perm_ids = request.POST.getlist('permissions')
            user.user_permissions.set(Permission.objects.filter(id__in=perm_ids))
            return redirect('edit_user')  
    else:
        form = EditUserForm(instance=user, user=request.user)

    return render(request, 'edit_user.html', {'form': form})


@login_required
def edit_user_list(request, pk):
    edit_user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=edit_user, user=request.user)
        if form.is_valid(): 
            new_password = form.cleaned_data.get('password')

            # 🔹 อัปเดตเฉพาะกรณีกรอกรหัสผ่านใหม่
            if new_password:
                edit_user.set_password(new_password)
            else:
                # ✅ เก็บ password เดิมไว้
                edit_user.password = CustomUser.objects.get(pk=pk).password

            form.save()

            # Update user permissions
            perm_ids = request.POST.getlist('permissions')
            edit_user.user_permissions.set(Permission.objects.filter(id__in=perm_ids))

            return redirect('user_list')
    else:
        form = EditUserForm(request.POST or None, request.FILES or None, instance=edit_user)

    return render(request, 'edit_user.html', {'form': form})
 
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def group_list_view(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def group_create_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully.")
            return redirect('group_list')
    else:
        form = GroupForm()

    return render(request, 'group_form.html', {'form': form})



@login_required
def group_edit_view(request, group_id):
    if group_id:
        group = get_object_or_404(Group, id=group_id)
    else:
        group = Group()

    form = GroupForm(request.POST or None, instance=group)

    if request.method == 'POST':
        if form.is_valid():
            group = form.save(commit=False)
            group.save()

            selected_permissions = request.POST.getlist('permissions')
            group.permissions.set(Permission.objects.filter(id__in=selected_permissions))
            group.save()
            return redirect('group_list')  # เปลี่ยนเป็น path ที่คุณต้องการ

    return render(request, 'group_form.html', {'form': form})

# 🗑️ ลบกลุ่ม
@login_required
def group_delete_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully.")
    return redirect('group_list')

