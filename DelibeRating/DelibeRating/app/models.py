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
    username = models.CharField(max_length=254,primary_key=True)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        #verbose_name = ('user')
        managed = False
        db_table = 'app_customuser'