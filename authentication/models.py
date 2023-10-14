from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=180, default='')
