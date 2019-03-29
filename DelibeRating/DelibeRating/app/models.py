"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    identifier = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    USERNAME_FIELD = 'identifier'

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')