import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aidat_takip.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Resident

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    Resident.objects.get_or_create(
        user=user,
        defaults={
            'first_name': 'Site',
            'last_name': 'Yöneticisi',
            'flat_number': 0,
            'phone_number': '0000000000'
        }
    )
    print("Admin user 'admin' created with password 'admin123'")
else:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print("Admin user 'admin' already existed, password reset to 'admin123'")
