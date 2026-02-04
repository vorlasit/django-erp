from django.urls import path 
from . import views

urlpatterns = [
    path('request_list/<str:req_type>/', views.request_list, name='request_list'), 
    path('request_list_all//<str:req_type>/', views.request_list_all, name='request_list_all'),
    path('request_create/<str:req_type>/', views.request_create, name='request_create'),
    path('request_edit/<int:request_id>/', views.request_edit, name='request_edit'),
    path('request_delete/<int:request_id>/', views.request_delete, name='request_delete'),
    
    path('ajax/users-by-department/', views.ajax_users_by_department, name='users_by_department'),
    path('request_main/', views.request_main, name='request_main'),

]