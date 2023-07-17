"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db import models, connection
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    """Custom User Model, extending AbstractUser
        username, email, password, first_name, last_name, groups
    """
    username = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    stars = models.CharField(max_length=10000)
    likes = models.CharField(max_length=10000)
    tastes = models.CharField(max_length=50000, default='{}')
    dislikes = models.CharField(max_length=10000)

    class Meta:
        managed = False
        db_table = 'app_customuser'
        #Implement for delete user
        #permissions = (
        #    ('delete', 'can delete')
        #    )

class CustomGroupQuerySet(models.query.QuerySet):
    def get(self, gid):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name, group_id
	                FROM public.app_customgroup
                    WHERE group_id = %s""", [gid])
                result_list = []
                for row in cursor.fetchall():
                    cg = self.model(name=row[0], group_id=row[1])
            return cg
        except:
            return None

    def create(self, name, gid):
        try:
            obj = CustomGroup()
            obj.group_id = gid
            obj.name = name
            obj.save()
            return obj
        except:
            return None

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

    def get(self, gid):
        return self.get_queryset().get(gid)

    def create(self, name, gid):
        return self.get_queryset().create(name, gid)

    def all(self):
        return self.get_queryset().all()

class CustomGroup(models.Model):
    """Custom Group Model, extending AbstractUser
        owner, name
    """
    name = models.CharField(max_length=50, primary_key=True)

    group = models.OneToOneField(Group, unique=True, on_delete=models.CASCADE)

    objects = CustomGroupManager()

    class Meta:
        ordering = ['name']
        db_table = 'app_customgroup'

class GroupVoteQuerySet(models.query.QuerySet):
    def get(self, vid):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT vote_id, name, group_id, vote_options
	                FROM public.app_votes
                    WHERE vote_id = %s""", [vid])

                for row in cursor.fetchall():
                    gv = self.model(vote_id=row[0], name=row[1], group_id=row[2], vote_options = row[3])
            return gv
        except:
            return None

    def get_or_create(self, vid, nam, grp):
        try:
            print(f"Getting {vid}")
            obj = self.get(vid)
            if obj:
                return obj, False
            else:
                raise GroupVote.DoesNotExist
        except GroupVote.DoesNotExist:
            print("Group doesn't exist")
            obj = GroupVote()
            obj.vote_id = vid
            obj.name = nam
            obj.group = grp
            obj.vote_options = ''
            obj.save()
            return obj, True
        except:
            return None, False
    
    def get_options(self, vid):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT opt_id, group_vote_id, business_id, upvotes, downvotes
	            FROM public.app_vote_options
                WHERE group_vote_id = %s""", [vid])
            result_list = []
            for row in cursor.fetchall():
                vo = VoteOption(opt_id=row[0], group_vote_id=row[1], business_id=row[2], upvotes=row[3], downvotes=row[4])
                result_list.append(vo)
        return result_list

    def all_active(self, gid):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT vote_id, name, group_id, vote_options
	            FROM public.app_votes
                WHERE group_id = %s""", [gid])
            result_list = []
            for row in cursor.fetchall():
                gv = self.model(vote_id=row[0], name=row[1], group_id=row[2], vote_options = row[3])
                result_list.append(gv)
        return result_list

    def all(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT vote_id, name, group_id, vote_options
	            FROM public.app_votes""")
            result_list = []
            for row in cursor.fetchall():
                gv = self.model(vote_id=row[0], name=row[1], group_id=row[2], vote_options = row[3])
                result_list.append(gv)
        return result_list

class GroupVoteManager(models.Manager):
    def get_queryset(self):
        return GroupVoteQuerySet(self.model)

    def get(self, vid):
        return self.get_queryset().get(vid)

    def get_or_create(self, vid, nam, grp):
        return self.get_queryset().get_or_create(vid, nam, grp)

    def get_options(self, vid):
        return self.get_queryset().get_options(vid)

    def all_active(self, gid):
        return self.get_queryset().all_active(gid)

    def all(self):
        return self.get_queryset().all()

class GroupVote(models.Model):
    """Group Vote, consisting of multiple Vote Options
    """
    # MM-DD-YY--<Name>
    vote_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    vote_options = models.CharField(max_length=10000)

    objects = GroupVoteManager()

    class Meta:
        db_table = 'app_votes'

class VoteOptionQuerySet(models.query.QuerySet):
    def get(self, gvid, oid):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT opt_id, group_vote_id, business_id, upvotes, downvotes
	                FROM public.app_vote_options
                    WHERE group_vote_id = %s AND opt_id = %s""", [gvid, oid])
                result_list = []

                for row in cursor.fetchall():
                    vo = self.model(opt_id=row[0], group_vote_id=row[1], business_id=row[2], upvotes=row[3], downvotes=row[4])
            return vo
        except:
            return None

    def vote_count(self, oid):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT opt_id, group_vote_id, business_id, upvotes, downvotes
	                FROM public.app_vote_options
                    WHERE opt_id = %s""", [oid])
                result_list = []
                net_votes = 0

                for row in cursor.fetchall():
                    vo = self.model(opt_id=row[0], group_vote_id=row[1], business_id=row[2], upvotes=row[3], downvotes=row[4])
                if vo.upvotes:
                    for v in vo.upvotes[:-1].split(','):
                        net_votes += 1
                if vo.downvotes:
                    for d in vo.downvotes[:-1].split(','):
                        net_votes -= 1
            return net_votes
        except:
            return None

class VoteOptionManager(models.Manager):
    def get_queryset(self):
        return VoteOptionQuerySet(self.model)

    def get(self, gvid, oid):
        return self.get_queryset().get(gvid, oid)

    def vote_count(self, oid):
        return self.get_queryset().vote_count(oid)

class VoteOption(models.Model):
    """Vote Option, associated with a Group Vote
    """
    opt_id = models.CharField(max_length=50, primary_key=True)
    group_vote = models.ForeignKey(GroupVote, on_delete=models.CASCADE)
    business_id = models.CharField(max_length=50)
    upvotes = models.CharField(max_length=2000)
    downvotes = models.CharField(max_length=2000)

    objects = VoteOptionManager()

    class Meta:
        db_table = 'app_vote_options'