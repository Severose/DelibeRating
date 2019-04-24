"""
Definition of views.
"""

import operator
import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.template import RequestContext
from datetime import datetime
from app.forms import *
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.hashers import PBKDF2PasswordHasher as hasher
from django.contrib.auth.hashers import make_password
from time import sleep
from yelpapi import YelpAPI
import argparse
from pprint import pprint
from django.conf import settings
import json
from django.core.cache import cache
from django.core.paginator import Paginator

yelp_api = YelpAPI(settings.API_KEY, timeout_s=3.0)

def home(request):
    """Renders the home page.
        TODO: Update content
    """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
        {
            'title':'Home Page',
        }
    )

def login(request):
    """Renders the login page."""
    print("Login View")
    if request.method == 'POST':
        print("Login: POST Request")
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            print("Login: Form Valid")
            user = auth_authenticate(username=request.POST['username'].lower(),
                                     password=request.POST['password'])
            auth_login(request,user)
            print(request.user.last_login)
            return redirect('/')
        else:
            print("Login: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Login: GET Request")
        form = CustomUserAuthenticationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        {
            'title':'Login',
            'message':'Login to your account.',
            'form': form,
        }
    )

def register(request):
    """Renders the register page."""
    print("Register View")
    if request.method == 'POST':
        print("Register: POST Request")
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            print("Register: Form Valid")
            form.save()
            messages.success(request, 'Your account was successfully created!')
            return redirect('/')
        else:
            print("Register: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Register: GET Request")
        form = CustomUserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/register.html',
        {
            'title':'Register',
            'message':'Register a new user account.',
            'form':form,
        }
    )

def search(request):
    """Renders the search page.
        TODO: Update content
    """
    print("Search View")

    if request.method == 'GET':
        query = request.GET.get('q', None)

        if 'q' in request.GET:
            print(request.GET)
        else:
            print('q not found!')

        if cache.get(query):
            print("Using cached results!")
            raw_data = cache.get(query)
        else:
            print("Querying Yelp Fusion API")
            raw_data = str(yelp_api.search_query(term=query, location='irvine, ca', sort_by='distance', limit=24))
            data = json.loads(json.dumps(raw_data))
            cache.set(query, data, 86400)  #TODO: Use DEFAULT_TIMEOUT

        print(data)
        page = request.GET.get('page', 1)
        paginator = Paginator(raw_data, 12)

        results = paginator.page(page)

        print("Settings: GET Request")
        context = {'title':'Search',
                   'message':'Search Page',
                   'results':results,
                  }
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/search.html',
            context
        )
    else:
        return render(request,"app/search.html",{})

@login_required
def settings(request):
    """Renders the edit account info page.
        TODO: Implement changing account information
    """
    print("Settings View")
    if request.method == 'POST':
        print("Settings: POST Request")
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Settings changed.')
            return redirect('settings')
        else:
            print("Settings: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Settings: GET Request")
        form = CustomUserChangeForm(instance=request.user)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settings.html',
        {
            'title':'Settings',
            'message':'Your settings page.',
            'form':form,
        }
    )

@login_required
def password(request):
    """Renders the edit account info page.
        TODO: Implement changing password
    """
    print("Password View")
    if request.method == 'POST':
        print("Password: POST Request")
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, 'Password changed.')
            return redirect('password')
        else:
            print("Password: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Password: GET Request")
        form = CustomPasswordChangeForm(request.user)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/password.html',
        {
            'title':'Password',
            'message':'Change password page.',
            'form':form,
        }
    )

@staff_member_required
def delete_user(request, username):
    """Delete user view (NO TEMPLATE)
        TODO: Actually delete users
    """
    context = {}

    try:
        user = CustomUser.objects.get(username = username)
        user.delete()
        context['msg'] = 'The user is deleted.'            

    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")    
        context['msg'] = 'User does not exist.'

    except Exception as e: 
        pass

    return render(request, 'home.html', context=context)