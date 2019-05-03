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
    url(r'^api/search/', app_views.yelp_autocomplete, name='yelp_autocomplete'),
    url(r'^api/users/', app_views.user_autocomplete, name='user_autocomplete'),
    url(r'^group/api/users/', app_views.user_autocomplete, name='user_autocomplete'), #Kludge
    url(r'^create_group', app_views.create_group, name='create_group'),
    url(r'^group', app_views.group, name='group'),
    url(r'^login/$', app_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/',}, name='logout'),
    url(r'^random', app_views.randomizer, name='random'),
    url(r'^register', app_views.register, name='register'),
    url(r'^password', app_views.password, name='password'),
    url(r'^search/$', app_views.search, name='search'),
    url(r'^settings', app_views.settings, name='settings'),
    url(r'^suggestions', app_views.suggestions, name='suggestions'),
    url(r'^profile', app_views.profile, name='profile'),
    url(r'^vote', app_views.vote, name='vote'),
    url(r'^delete_user/(?P<username>[\w|\W.-]+)/$', app_views.delete_user, name='delete-user'), 

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
