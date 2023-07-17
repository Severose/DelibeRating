"""
Definition of urls for DelibeRating.
"""

from datetime import datetime
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
import app.forms as app_forms
import app.views as app_views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    re_path(r'^$', app_views.home, name='home'),
    re_path(r'^api/addopt', app_views.addopt, name='addopt'),
    re_path(r'^api/dislike', app_views.dislike, name='dislike'),
    re_path(r'^api/downvote', app_views.downvote, name='downvote'),
    re_path(r'^api/like', app_views.like, name='like'),
    re_path(r'^api/search/', app_views.yelp_autocomplete, name='yelp_autocomplete'),
    re_path(r'^api/star', app_views.star, name='star'),
    re_path(r'^api/upvote', app_views.upvote, name='upvote'),
    re_path(r'^api/update_chart', app_views.update_chart, name='update_chart'),
    re_path(r'^api/users/', app_views.user_autocomplete, name='user_autocomplete'),
    re_path(r'^group/api/users/', app_views.user_autocomplete, name='user_autocomplete'), #Kludge
    re_path(r'^group/vote/create', app_views.create_group_vote, name='create_group_vote'),
    re_path(r'^group/create', app_views.create_group, name='create_group'),
    re_path(r'^group/manage', app_views.group_manage, name='group_manage'),
    re_path(r'^group/vote', app_views.group_vote, name='group_vote'),
    re_path(r'^group', app_views.group, name='group'),
    re_path(r'^login/$', app_views.login, name='login'),
    re_path(r'^logout$', auth_views.auth_logout, {'next_page': '/',}, name='logout'),
    re_path(r'^search/random', app_views.randomizer, name='random'),
    re_path(r'^random', app_views.randomizer, name='random'),
    re_path(r'^register', app_views.register, name='register'),
    re_path(r'^password', app_views.password, name='password'),
    re_path(r'^search/$', app_views.search, name='search'),
    re_path(r'^settings', app_views.settings, name='settings'),
    re_path(r'^suggestions', app_views.suggestions, name='suggestions'),
    re_path(r'^profile', app_views.profile, name='profile'),
    re_path(r'^voting', app_views.voting, name='voting'),
    re_path(r'^delete_user', app_views.delete_user, name='delete_user'), 

    # Uncomment the admin/doc line below to enable admin documentation:
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),
]
