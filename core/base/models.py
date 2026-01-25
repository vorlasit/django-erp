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