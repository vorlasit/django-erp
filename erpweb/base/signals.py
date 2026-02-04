from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission 
from .models import User


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    admin_group, _ = Group.objects.get_or_create(name='Administrator')
    user_group, _ = Group.objects.get_or_create(name='User')

    # Administrator = all permissions
    admin_group.permissions.set(Permission.objects.all())

    # User = limited permissions (example)
    user_permissions = Permission.objects.filter(
        codename__in=[
            'view_user',
            'change_user',
        ]
    )
    user_group.permissions.set(user_permissions)


@receiver(post_save, sender=User)
def set_first_user_as_admin(sender, instance, created, **kwargs):
    if not created:
        return 
    # ถ้าเป็น user คนแรกในระบบ
    if User.objects.count() == 1:
        admin_group = Group.objects.get(name='Administrator')
        instance.groups.add(admin_group)

        # (แนะนำ) ให้เป็น superuser ด้วย
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
    else:
        # เพิ่ม user ใหม่ในกลุ่ม User โดยอัตโนมัติ
        user_group = Group.objects.get(name='User')
        instance.groups.add(user_group)