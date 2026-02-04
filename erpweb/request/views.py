from django.shortcuts import render, redirect, get_object_or_404
from .models import Request
from .forms import RequestForm
from base.models import User
from django.http import JsonResponse

def request_list(request, req_type):
    requests = Request.objects.all().order_by('id')
    if req_type:
        requests = requests.filter(type=req_type) 
    return render(request, 'request_list.html', {'requests': requests, 'req_type': req_type})

def request_list_all(request, req_type=None):
    requests = Request.objects.all().order_by('id')  
    return render(request, 'request_list.html', {'requests': requests, 'req_type': req_type})

def request_create(request,req_type): 
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.requester = request.user
            obj.save()
            return redirect('request_list', req_type=req_type)
    else:
        # กรณี GET → ส่ง initial ให้ form
        form = RequestForm(initial={'type': req_type})
    return render(request, 'request_form.html', {'form': form ,})

def ajax_users_by_department(request):
    dept_id = request.GET.get('department') 
    users = User.objects.filter(
        department_id=dept_id
    ).values('id', 'username')
    return JsonResponse(list(users), safe=False)

def request_edit(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id) 
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            return redirect('request_list', req_type=request_obj.type)
    else:
        form = RequestForm(instance=request_obj)
    return render(request, 'request_form.html', {'form': form})

def request_delete(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id) 
    request_obj.delete()
    return redirect('request_list', req_type=request_obj.type)

def request_main(request): 
    type_choices = [
        {
            'type': 'helpdesk',
            'name': 'Helpdesk',
            'icon': 'icon/helpdesk.png', 
        },
        {
            'type': 'equipment',
            'name': 'Equipment',
            'icon': 'icon/equipment.png', 
        },
        {
            'type': 'device',
            'name': 'Device',
            'icon': 'icon/device.png', 
        },
        {
            'type': 'return',
            'name': 'return',
            'icon': 'icon/return.png', 
        },
    ]
    
    return render(request, 'request_main.html', {'req_type': type_choices})
