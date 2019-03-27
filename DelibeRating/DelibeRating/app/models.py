"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    identifier = models.CharField(max_length=40, unique=True)
    USERNAME_FIELD = 'identifier'