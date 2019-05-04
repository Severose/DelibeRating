"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from vote.models import VoteModel

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
    username = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'app_customuser'

class VoteOption(models.Model):
    """Vote Option in Group Vote
    """
    business_name = models.CharField(primary_key=True)

class GroupVote(VoteModel, models.Model):
    """Group Vote, consisting of multiple Vote Options
    """
    vote_option = models.ForeignKey(VoteOption)

    class Meta:
        db_table = 'app_votes'