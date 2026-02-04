from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django_user_agents.utils import get_user_agent
from .models import UserLoginSession

class TrackUserSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_agent = get_user_agent(request)
            UserLoginSession.objects.update_or_create(
                user=request.user,
                session_key=request.session.session_key,
                defaults={
                    "ip_address": request.META.get('REMOTE_ADDR'),
                    "user_agent": request.META.get('HTTP_USER_AGENT', ''),
                    "device": user_agent.device.family,
                    "browser": user_agent.browser.family,
                    "os": user_agent.os.family,
                }
            )

class LoginRequiredMiddleware:
    """
    Middleware ที่จะ redirect ผู้ใช้ไปหน้า login ถ้ายังไม่ได้ login
    ยกเว้นบาง path ที่อนุญาต เช่น login และ register
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            return self.get_response(request)
        
        allowed_paths = [
            reverse('login'),
            reverse('register'),
        ]

        # ตรวจสอบถ้ายังไม่ login และ path ไม่อยู่ใน allowed_paths
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('login')

        response = self.get_response(request)
        return response