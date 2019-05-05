"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models, connection
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomGroupQuerySet(models.query.QuerySet):
    def get(self, id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT owner_id, name, group_id
	                FROM public.app_customgroup
                    WHERE group_id = %s""", [gid])
                result_list = []
                for row in cursor.fetchall():
                    cg = self.model(owner_id=row[0], name=row[1], group_id=row[2])
                    result_list.append(cg)
            return result_list
        except:
            return CustomGroup()

    def create(self, name, gid, oid):
        try:
            obj = CustomGroup()
            obj.group = gid
            obj.name = name
            obj.owner_id = oid
            obj.save()
            return obj
        except:
            return CustomGroup()

    def all(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT owner_id, name, group_id
	            FROM public.app_customgroup""")
            result_list = []
            for row in cursor.fetchall():
                cg = self.model(owner_id=row[0], name=row[1], group_id=row[2])
                result_list.append(cg)
        return result_list

class CustomGroupManager(models.Manager):
    def get_queryset(self):
        return CustomGroupQuerySet(self.model)

    def get(self, id):
        return self.get_queryset().get(id)

    def create(self, name, gid, oid):
        return self.get_queryset().get_or_create(name, gid, oid)

    def all(self):
        return self.get_queryset().all()

class CustomGroup(models.Model):
    """Custom Group Model, extending AbstractUser
        owner, name
    """
    name = models.CharField(max_length=50, primary_key=True)
    group = models.OneToOneField(Group, unique=True)
    objects = CustomGroupManager()

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
    def get(self, vid):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT vote_id, group_id
	                FROM public.app_votes
                    WHERE vote_id = %s""", [vid])
                result_list = []

                #if row in cursor.fetchall():
                for row in cursor.fetchall():
                    gv = self.model(vote_id=row[0], group_id=row[1])
            return gv
        except:
            return None

    def get_or_create(self, vid, grp):
        try:
            obj = self.get(vid)
            if obj:
                return obj, False
            else:
                raise GroupVote.DoesNotExist
        except GroupVote.DoesNotExist:
            obj = GroupVote()
            obj.vote_id = vid
            obj.group = grp
            obj.save()
            return obj, True
        except:
            return GroupVote(), False

    def all_active(self, gid):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT vote_id, group_id
	            FROM public.app_votes
                WHERE group_id = %s""", [gid])
            result_list = []
            for row in cursor.fetchall():
                gv = self.model(vote_id=row[0], group_id=row[1])
                result_list.append(gv)
        return result_list

    def all(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT vote_id, group_id
	            FROM public.app_votes""")
            result_list = []
            for row in cursor.fetchall():
                gv = self.model(vote_id=row[0], group_id=row[1])
                result_list.append(gv)
        return result_list

class GroupVoteManager(models.Manager):
    def get_queryset(self):
        return GroupVoteQuerySet(self.model)

    def get(self, vid):
        return self.get_queryset().get(vid)

    def get_or_create(self, vid, grp):
        return self.get_queryset().get_or_create(vid, grp)

    def all_active(self, gid):
        return self.get_queryset().all_active(gid)

    def all(self):
        return self.get_queryset().all()

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