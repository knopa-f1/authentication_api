import os
import django
from django.contrib.auth import get_user_model
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

User = get_user_model()

email = config('SUPERUSER_EMAIL')
password = config('SUPERUSER_PASSWORD')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)

print(f"Superuser {email} created.")