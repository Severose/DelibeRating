"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomGroup(models.Model):
    """Custom Group Model, extending AbstractUser
        username, email, password, first_name, last_name
    """
    group = models.OneToOneField(Group)
    groupname = models.CharField(max_length=50,primary_key=True)
    members = models.ManyToManyField(CustomUser)

    class Meta:
        managed = False
        db_table = 'app_customgroup'

class CustomUser(AbstractUser):
    """Custom User Model, extending AbstractUser
        username, email, password, first_name, last_name
    """
    username = models.CharField(max_length=254,primary_key=True)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    groups = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'app_customuser'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)