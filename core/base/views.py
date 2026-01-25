from django.shortcuts import render,redirect, get_object_or_404
from .form import (AppSettingsForm)  
from .models import AppSettings
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
def settings_view(request):
    settings = AppSettings.get_settings()
    if request.method == "POST":
        form = AppSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
        return redirect("settings")  # reload after save
    else:
        form = AppSettingsForm(instance=settings)

    icons = AppSettings.objects.all()

    return render(request, "setting.html", {"form": form, 'icons':icons})

@login_required
def dashboard(request): 
    total_users = CustomUser.objects.count()  
    # Orders per month (last 12 months) 

    context = { 
        'total_users': total_users,  
    }
    return render(request, 'dashboard.html', context) 
