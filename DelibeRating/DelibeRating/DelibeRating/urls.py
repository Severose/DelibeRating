"""
Definition of urls for DelibeRating.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
import app.forms as app_forms
import app.views as app_views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^$', app_views.home, name='home'),
    url(r'^api/addopt', app_views.addopt, name='addopt'),
    url(r'^api/dislike', app_views.dislike, name='dislike'),
    url(r'^api/downvote', app_views.downvote, name='downvote'),
    url(r'^api/like', app_views.like, name='like'),
    url(r'^api/search/', app_views.yelp_autocomplete, name='yelp_autocomplete'),
    url(r'^api/star', app_views.star, name='star'),
    url(r'^api/upvote', app_views.upvote, name='upvote'),
    url(r'^api/update_chart', app_views.update_chart, name='update_chart'),
    url(r'^api/users/', app_views.user_autocomplete, name='user_autocomplete'),
    url(r'^group/api/users/', app_views.user_autocomplete, name='user_autocomplete'), #Kludge
    url(r'^group/vote/create', app_views.create_group_vote, name='create_group_vote'),
    url(r'^group/create', app_views.create_group, name='create_group'),
    url(r'^group/manage', app_views.group_manage, name='group_manage'),
    url(r'^group/vote', app_views.group_vote, name='group_vote'),
    url(r'^group', app_views.group, name='group'),
    url(r'^login/$', app_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/',}, name='logout'),
    url(r'^search/random', app_views.randomizer, name='random'),
    url(r'^random', app_views.randomizer, name='random'),
    url(r'^register', app_views.register, name='register'),
    url(r'^password', app_views.password, name='password'),
    url(r'^search/$', app_views.search, name='search'),
    url(r'^settings', app_views.settings, name='settings'),
    url(r'^suggestions', app_views.suggestions, name='suggestions'),
    url(r'^profile', app_views.profile, name='profile'),
    url(r'^voting', app_views.voting, name='voting'),
    url(r'^delete_user', app_views.delete_user, name='delete_user'), 

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
