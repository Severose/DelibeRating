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
        owner, name
    """
    name = models.CharField(max_length=50, primary_key=True)
    group = models.OneToOneField(Group, unique=True)

    class Meta:
        ordering = ['name']
        db_table = 'app_customgroup'

class CustomUser(AbstractUser):
    """Custom User Model, extending AbstractUser
        username, email, password, first_name, last_name, groups
    """
    username = models.CharField(max_length=254, primary_key=True)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'app_customuser'

class GroupMember(models.Model):
    member = models.ForeignKey(CustomUser)
    group = models.ForeignKey(CustomGroup)

class GroupProfile(models.Model):
    group = models.OneToOneField(CustomGroup)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)