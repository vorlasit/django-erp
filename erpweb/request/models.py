from django.db import models
from base.models import User, Department

# Create your models here.
class Request(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type_choices = [
        ('helpdesk', 'Helpdesk'),
        ('equipment', 'Equipment'),
        ('device', 'Device'),
        ('return', 'Return')
    ]
    type = models.CharField(max_length=100, blank=True, null=True,choices=type_choices )
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='requests')
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=50, default='pending',choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ])

    def __str__(self):
        return self.title
