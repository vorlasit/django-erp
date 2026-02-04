from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [  
    path('close-session/<int:session_id>/', views.close_session, name='close_session'), 
    path('main_menu/', views.main_menu, name='main_menu'), 
    path('register/', views.register_view, name='register'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('', views.dashboard, name='dashboard'),  
    path("settings/", views.settings_view, name="settings"),
    path('profile/', views.profile, name='profile'), 
    path('users/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('register_on_system/', views.register_on_system, name='register_on_system'),
    path('export_users_excel/', views.export_users_excel, name='export_users_excel'),
    path('import_users_excel/', views.import_users_excel, name='import_users_excel'),
    path('user/<int:user_id>/change-password/', views.change_password, name='change_password'),
    path('groups/', views.group_list, name='group_list'),
    path('create_group/', views.group_create, name='group_create'),
    path('edit_group/<int:group_id>/', views.group_edit, name='group_edit'),
    path('delete_group/<int:group_id>/', views.group_delete, name='group_delete'),
    
    path('departments/', views.department_list, name='department_list'),
    path('create_department/', views.department_create, name='department_create'),
    path('edit_department/<int:department_id>/', views.department_edit, name='department_edit'),
    path('delete_department/<int:department_id>/', views.department_delete, name='department_delete'),
]