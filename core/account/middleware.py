from django.shortcuts import redirect
from django.urls import reverse

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