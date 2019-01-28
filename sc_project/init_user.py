# init superuser
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='sc').exists():
    user=User.objects.create_user('sc', password='password')
    user.is_superuser=True
    user.is_staff=True
    user.save()
