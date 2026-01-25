from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [  
    path('register/', views.register_view, name='register'),
    path('user_list/', views.user_list, name='user_list'),
    path('user/<int:pk>/edit/', views.edit_user_list, name='edit_user_list'),
    path('edit/', views.edit_user, name='edit_user'), 
    path('profile/', views.profile, name='profile'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # auth views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('groups/', views.group_list_view, name='group_list'),
    path('groups/add/', views.group_create_view, name='group_create'),
    path('groups/<int:group_id>/edit/', views.group_edit_view, name='group_edit'),
    path('groups/<int:group_id>/delete/', views.group_delete_view, name='group_delete'), 

]