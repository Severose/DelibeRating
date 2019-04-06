"""
Definition of urls for DelibeRating.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from app import views as app_views
from app import forms as app_forms

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^todo', app.views.todo, name='todo'),
    url(r'^login/$', app_views.login, name='login'),
    url(r'^logout$',
        auth_views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^register', app.views.register, name='register'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
