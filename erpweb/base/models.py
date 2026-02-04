from django.contrib.auth.models import AbstractUser
from django.db import models 
# Create your models here. 
def favicon_upload_to(instance, filename):
    # จะบันทึกไฟล์เป็น media/icons/favicon.png เสมอ
    return "icons/favicon.png"

class AppSettings(models.Model):
    name = models.CharField(max_length=100, default="My Django App")
    favicon = models.ImageField(upload_to=favicon_upload_to, blank=True, null=True)
    app_icon = models.ImageField(upload_to="icons/", blank=True, null=True)

    class Meta:
        verbose_name = "App Setting"
        verbose_name_plural = "App Settings"

    def __str__(self):
        return self.name

    @classmethod
    def get_settings(cls):
        return cls.objects.first() or cls.objects.create()
    
class User(AbstractUser): 
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserLoginSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=256)
    device = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} on {self.device} ({self.browser})"