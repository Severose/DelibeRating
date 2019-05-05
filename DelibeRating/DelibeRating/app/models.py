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
    username = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'app_customuser'

class GroupVoteQuerySet(models.query.QuerySet):
    def get_or_create(self, obj):
        try:
            group_vote = GroupVote.objects.get(vote_id = obj.vote_id)
            return group_vote, False
        except GroupVote.DoesNotExist:
            obj.save()
            return group_vote, True

class GroupVoteManager(models.Manager):
    def get_queryset(self):
        return GroupVoteQuerySet(self.model)

class GroupVote(models.Model):
    """Group Vote, consisting of multiple Vote Options
    """
    # MM-DD-YY--<Name>
    vote_id = models.CharField(max_length=30, primary_key=True)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    objects = GroupVoteManager()

    class Meta:
        db_table = 'app_votes'
        
class VoteOption(models.Model):
    """Vote Option in Group Vote
    """
    business_name = models.CharField(max_length=100, primary_key=True)
    # Add JSON object for business
    group_vote = models.ForeignKey(GroupVote, on_delete=models.CASCADE)