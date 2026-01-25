from django.db import models
from django.contrib.auth.models import AbstractUser ,Group

# Create your models here.

class CustomUser(AbstractUser):
    company = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

