"""
Definition of views.
"""

import operator
import random
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
from django import template

registerT = template.Library()
yelp_api = YelpAPI(settings.API_KEY, timeout_s=3.0)

@login_required
def create_group(request):
    """Renders the create group page."""
    print("Create Group View")
    time_form = CustomTimeForm()

    if request.method == 'POST':
        print("Create Group: POST Request")
        form = CustomGroupCreationForm(data=request.POST)
        if form.is_valid():
            print("Create Group: Form Valid")
            group, created = Group.objects.get_or_create(name=form.cleaned_data['name'])
            user = request.user
            if created:
                user.groups.add(group)
                group.save()
                messages.success(request, 'Your group was successfully created!')
            else:
                messages.error(request, 'That group already exists!')
            return redirect('group/?g=' + group.name)
        else:
            print("Create Group: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Register: GET Request")
        form = CustomGroupCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/create_group.html',
        {
            'title':'Create Group',
            'form':form,
            'time_form': time_form,
        }
    )

@login_required
def group(request):
    """Renders the group page.
        TODO: Implement
    """
    print("Group View")
    time_form = CustomTimeForm()

    if request.method == 'GET':
        print("Group: GET Request")
        form = CustomGroupChangeForm()
        groupname = request.GET.get('g', None)

        if 'g' in request.GET:
            print(request.GET)
        else:
            print('g not found!')

        group = Group.objects.get(name = groupname)
        users = CustomUser.objects.filter(groups__name=groupname)
    else:
        print("Group: POST Request")
        form = CustomGroupChangeForm(data=request.POST)
        if form.is_valid():
            print("Group: Form Valid")
            groupname = request.GET.get('g', None)

            if 'g' in request.GET:
                print(request.GET)
            else:
                print('g not found!')

            group = Group.objects.get(name = groupname)
            user = CustomUser.objects.get(username=form.cleaned_data['username'])
            users = CustomUser.objects.filter(groups__name=groupname)
            user.groups.add(group)
            group.save()
            messages.success(request, 'Your group was successfully created!')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/group.html',
        {
            'title':'Group',
            'time_form': time_form,
            'form': form,
            'group': group,
            'users': users,
        }
    )

def home(request):
    """Renders the home page.
        TODO: Update content
    """
    print("Home View")
    time_form = CustomTimeForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
        {
            'title':'Home Page',
            'time_form': time_form,
        }
    )

def login(request):
    """Renders the login page."""
    print("Login View")
    time_form = CustomTimeForm()

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
            'form': form,
            'time_form': time_form,
        }
    )

@login_required
def password(request):
    """Renders the edit account info page.
        TODO: Implement changing password
    """
    print("Password View")
    time_form = CustomTimeForm()

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
            'form':form,
            'time_form': time_form,
        }
    )

@login_required
def profile(request):
    """Renders the user profile info page.
        TODO: Implement
    """
    print("User Profile View")
    time_form = CustomTimeForm()
    groups = []

    if request.method == 'GET':
        print("User Profile: GET Request")
        name = request.GET.get('u', None)

        if 'u' in request.GET:
            print(request.GET)
        else:
            print('u not found!')
    else:
        print("User Profile: POST Request")
        name = ""

    user = CustomUser.objects.get(username = name)
    for g in user.groups.all():
        groups.append(g.name)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/profile.html',
        {
            'title':'Profile',
            'time_form': time_form,
            'user': user,
            'groups': groups,
        }
    )

def randomizer(request):
    """Renders the randomizer page.
        TODO: Implement
    """
    print("Randomizer View")
    time_form = CustomTimeForm()
    rindex = 0

    if request.method == 'GET':
        query = request.GET.get('q', None)
        location = request.GET.get('loc', None)
        radius = request.GET.get('rad', None)
        sortby = request.GET.get('sort', None)
        pricerange = request.GET.get('price', None)
        opennow = request.GET.get('open', None)

        if 'q' in request.GET:
            print(request.GET)
        else:
            print('q not found!')

        if 'loc' in request.GET:
            print(request.GET)
        else:
            print('loc not found!')

        if 'rad' in request.GET:
            print(request.GET)
        else:
            print('rad not found!')

        if 'sort' in request.GET:
            print(request.GET)
        else:
            print('sort not found!')

        if 'price' in request.GET:
            print(request.GET)
        else:
            print('price not found!')

        if 'open' in request.GET:
            print(request.GET)
        else:
            print('open not found!')

        if cache.get(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum())):
            print("Using cached results!")
            print(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()))
            raw_data = cache.get(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()))
        else:
            print("Querying Yelp Fusion API")
            raw_data = yelp_api.search_query(term=query,
                                             location=location,
                                             radius=radius,
                                             limit=48,
                                             sort_by=sortby,
                                             price=pricerange,
                                             open_now=opennow)
            
        data = json.loads(json.dumps(raw_data))
        cache.set(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()), data, 86400)  #TODO: Use DEFAULT_TIMEOUT

        random.randint(0,len(data['businesses'])-1)

        results = [data['businesses'][random.randint(0,len(data['businesses']))]]

        print(results)

        print("Random: GET Request")
        context = {'title':'Randomizer',
                   'results':results,
                   'query':query,
                   'location':location,
                   'time_form': time_form,
                   'messages': messages,
                   }

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/random.html',
            context)

    else:
        return render(request,"app/random.html",{})

def register(request):
    """Renders the register page."""
    print("Register View")
    time_form = CustomTimeForm()

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
            'form':form,
            'time_form': time_form,
        }
    )

def search(request):
    """Renders the search page.
        TODO: Update content
    """
    print("Search View")
    time_form = CustomTimeForm()

    if request.method == 'GET':
        query = request.GET.get('q', None)
        location = request.GET.get('loc', None)
        radius = request.GET.get('rad', None)
        sortby = request.GET.get('sort', None)
        pricerange = request.GET.get('price', None)
        opennow = request.GET.get('open', None)

        if 'q' in request.GET:
            print(request.GET)
        else:
            print('q not found!')

        if 'loc' in request.GET:
            print(request.GET)
        else:
            print('loc not found!')

        if 'rad' in request.GET:
            print(request.GET)
        else:
            print('rad not found!')

        if 'sort' in request.GET:
            print(request.GET)
        else:
            print('sort not found!')

        if 'price' in request.GET:
            print(request.GET)
        else:
            print('price not found!')

        if 'open' in request.GET:
            print(request.GET)
        else:
            print('open not found!')

        if cache.get(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum())):
            print("Using cached results!")
            print(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()))
            raw_data = cache.get(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()))
        else:
            print("Querying Yelp Fusion API")
            raw_data = yelp_api.search_query(term=query,
                                             location=location,
                                             radius=radius,
                                             limit=48,
                                             sort_by=sortby,
                                             price=pricerange,
                                             open_now=opennow)
            
        data = json.loads(json.dumps(raw_data))
        cache.set(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()), data, 86400)  #TODO: Use DEFAULT_TIMEOUT

        results_page = request.GET.get('page', 1)
        paginator = Paginator(data['businesses'], 12)

        results = paginator.page(results_page)

        print("Settings: GET Request")
        context = {'title':'Search',
                   'results':results,
                   'query':query,
                   'location':location,
                   'time_form': time_form,
                   }

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/search.html',
            context)

    else:
        return render(request,"app/search.html",{})

@login_required
def settings(request):
    """Renders the edit account info page.
        TODO: Implement changing account information
    """
    print("Settings View")
    time_form = CustomTimeForm()

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
            'form':form,
            'time_form': time_form,
        }
    )

def suggestions(request):
    """Renders the suggestions page.
        TODO: Implement
    """
    print("Suggestions View")
    time_form = CustomTimeForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/suggestions.html',
        {
            'title':'Suggestions Page',
            'time_form': time_form,
        }
    )

@login_required
def vote(request):
    """Renders the vote page.
        TODO: Implement
    """
    print("Vote View")
    time_form = CustomTimeForm()
    groups = []

    user = CustomUser.objects.get(username = request.user.username)
    for g in user.groups.all():
        groups.append(g.name)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/vote.html',
        {
            'title':'Group Vote Page',
            'time_form': time_form,
            'groups': groups,
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