from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # You can add custom fields here later (e.g., phone_number, avatar)
    # For now, we inherit username, email, password from AbstractUser
    pass