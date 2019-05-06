"""
Definition of views.
"""

import operator
import random
from random import shuffle
import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponse
from django.template import RequestContext
from datetime import datetime
from app.forms import *
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
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

def get_yelp_results(query,location,radius,sortby,pricerange,opennow,attributes):
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
                                         open_now=opennow,
                                         attributes=attributes)
            
    data = json.loads(json.dumps(raw_data))
    cache.set(''.join(i for i in str(query+location+radius+sortby+pricerange+opennow) if i.isalnum()), data, 86400)  #TODO: Use DEFAULT_TIMEOUT
    
    return data

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
            cgroup = CustomGroup.objects.create(form.cleaned_data['name'], group.id)
            user = request.user
            if created:
                user.groups.add(group)
                group.save()
                messages.success(request, 'Your group was successfully created!')
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
            'title': 'Create Group',
            'form': form,
            'time_form': time_form,
        }
    )

@login_required
def create_group_vote(request):
    """Renders the create vote page."""
    print("Create Vote View")
    time_form = CustomTimeForm()

    if request.method == 'POST':
        print("Create Vote: POST Request")
        form = CustomVoteCreationForm(data=request.POST)
        if form.is_valid():
            print("Create Vote: Form Valid")
            groupname = request.GET.get('g', None)
            group = Group.objects.get(name = groupname)
            cgroup = CustomGroup.objects.get(group.id)
            vote_id = datetime.datetime.now().strftime("%m-%d-%y--") + form.cleaned_data["name"]
            group_vote, created = GroupVote.objects.get_or_create(vote_id, cgroup)
            if created:
                messages.success(request, 'Your vote was successfully created!')
            return redirect('group/vote/?g=' + group.name + '&v=' + group_vote.vote_id)
        else:
            print("Create Vote: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Create Vote: GET Request")
        form = CustomVoteCreationForm()
        groupname = request.GET.get('g', None)
        group = Group.objects.get(name = groupname)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/create_group_vote.html',
        {
            'title': 'Create Vote',
            'form': form,
            'time_form': time_form,
            'group': group,
        }
    )

@login_required
def group(request):
    """Renders the group page.
        TODO: Implement
    """
    print("Group View")
    time_form = CustomTimeForm()
    active_votes = []

    if request.method == 'GET':
        print("Group: GET Request")
        form = CustomGroupChangeForm()
        groupname = request.GET.get('g', None)

        if 'g' in request.GET:
            print(request.GET)
        else:
            print('g not found!')

        group = Group.objects.get(name = groupname)
        cgroup = CustomGroup.objects.get(group.id)
        users = CustomUser.objects.filter(groups__name=groupname)
    else:
        print("Group: POST Request")
        form = CustomGroupChangeForm(data=request.POST)
        if form.is_valid():
            print("Group: Form Valid")
            if form.cleaned_data['act'] == 'add':
                group = Group.objects.get(name = form.cleaned_data['grp'])
                cgroup = CustomGroup.objects.get(group.id)
                user = CustomUser.objects.get(username = form.cleaned_data['usr'])
                if user.groups.filter(name=group.name).exists():
                    messages.error(request, 'User is already a member.')
                else:
                    user.groups.add(group)
                    group.save()
                users = CustomUser.objects.filter(groups__name=group.name)
            elif form.cleaned_data['act'] == 'rem':
                group = Group.objects.get(name = form.cleaned_data['grp'])
                cgroup = CustomGroup.objects.get(group.id)
                user = CustomUser.objects.get(username = form.cleaned_data['usr'])
                user.groups.remove(group)
                users = CustomUser.objects.filter(groups__name=group.name)
                
                if len(users) == 0:
                    return redirect('group')
                group.save()
            else:
                print('Error: unknown action')
                group = Group()
                cgroup = CustomGroup()
                users = []

            messages.success(request, 'Your group action was successful!')
    
    v_all = GroupVote.objects.all_active(cgroup.name)
    for v in v_all:
        active_votes.append(v.vote_id)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/group.html',
        {
            'title': 'Group',
            'time_form': time_form,
            'form': form,
            'group': group,
            'users': users,
            'active_votes': active_votes,
        }
    )

@login_required
def group_manage(request):
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
            if form.cleaned_data['act'] == 'add':
                group = Group.objects.get(name = form.cleaned_data['grp'])
                user = CustomUser.objects.get(username = form.cleaned_data['usr'])
                if user.groups.filter(name=group.name).exists():
                    messages.error(request, 'User is already a member.')
                else:
                    user.groups.add(group)
                    group.save()
                users = CustomUser.objects.filter(groups__name=group.name)
            elif form.cleaned_data['act'] == 'rem':
                group = Group.objects.get(name = form.cleaned_data['grp'])
                user = CustomUser.objects.get(username = form.cleaned_data['usr'])
                user.groups.remove(group)
                users = CustomUser.objects.filter(groups__name=group.name)
                
                if len(users) == 0:
                    return redirect('group')
                group.save()
            else:
                print('Error: unknown action')
                group = ''
                users = []

            messages.success(request, 'Your group action was successful!')
        

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/group_manage.html',
        {
            'title': 'Group',
            'time_form': time_form,
            'form': form,
            'group': group,
            'users': users,
        }
    )

@login_required
def group_vote(request):
    """Renders the group vote page."""
    print("Create Group View")
    time_form = CustomTimeForm()

    if request.method == 'POST':
        print("Create Group: POST Request")
        form = CustomGroupCreationForm(data=request.POST)
        if form.is_valid():
            print("Create Group: Form Valid")
            groupname = request.GET.get('g', None)
            groupvoteid = request.GET.get('v', None)
            group = Group.objects.get(name = groupname)
            group_vote = GroupVote.objects.get(groupvoteid)
            group = Group.objects.get(name=form.cleaned_data['name'])
            user = request.user
            if created:
                user.groups.add(group)
                group.save()
                messages.success(request, 'Your group was successfully created!')
            return redirect('group/?g=' + group.name)
        else:
            print("Create Group: Form Invalid")
            print(form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        print("Register: GET Request")
        groupname = request.GET.get('g', None)
        groupvoteid = request.GET.get('v', None)
        group = Group.objects.get(name = groupname)
        group_vote = GroupVote.objects.get(groupvoteid)
        form = CustomGroupCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/group_vote.html',
        {
            'title':'Create Group',
            'form':form,
            'time_form': time_form,
            'group': group,
            'group_vote': group_vote,
        }
    )

def home(request):
    """Renders the home page.
        TODO: Implement
    """
    print("Home View")
    time_form = CustomTimeForm()
    active_votes = []

    location = "Irvine, CA" #Update to use user's preferred location

    if request.method == 'GET':
        query = 'food'
        location = 'Irvine, CA'
        radius = '16100'
        sortby = 'rating'
        pricerange = '1,2,3,4'
        opennow = 'false'
        attributes = 'hot_and_new'

        data = get_yelp_results(query,location,radius,sortby,pricerange,opennow,attributes)

        user = request.user
        #for g in user.groups.all():
        #    cg = CustomGroup.objects.get(g.id)
        #    v_all = GroupVote.objects.all_active(cg.name)
        #    for v in v_all:
        #        active_votes.append(v.vote_id)


        shuffle(data['businesses'])

        results_page = request.GET.get('page', 1)
        paginator = Paginator(data['businesses'], 2)
        pages = []

        results = paginator.page(results_page)

        print("Home: GET Request")
        context = {'title':'Home',
                   'results':results,
                   'query':'',
                   'location':'Irvine, CA',
                   'time_form': time_form,
                   'pages': pages,
                   'user': user,
                   'active_votes': active_votes,
                   }

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/home.html',
            context)

    else:
        return render(request,"app/home.html",{})

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

        shuffle(data['businesses'])

        results = [data['businesses'][0]]

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
    active_votes = []

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

        data = get_yelp_results(query,location,radius,sortby,pricerange,opennow,"")
        user = request.user
        for g in user.groups.all():
            v_all = GroupVote.objects.all_active(g.name)
            for v in v_all:
                active_votes.append(v.vote_id)

        results_page = request.GET.get('page', 1)
        paginator = Paginator(data['businesses'], 12)
        pages = paginator.page_range

        results = paginator.page(results_page)

        print("Settings: GET Request")
        context = {'title':'Search',
                   'results':results,
                   'query':query,
                   'location':location,
                   'time_form': time_form,
                   'pages': pages,
                   'active_votes': active_votes,
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
        TODO: Update content
    """
    print("Suggestions View")
    time_form = CustomTimeForm()

    location = "Irvine, CA" #Update to use user's preferred location

    if request.method == 'GET':
        query = 'food'
        location = 'Irvine, CA'
        radius = '16100'
        sortby = 'rating'
        pricerange = '1,2,3,4'
        opennow = 'false'
        attributes = 'hot_and_new'

        data = get_yelp_results(query,location,radius,sortby,pricerange,opennow,attributes)
        shuffle(data['businesses'])

        results_page = request.GET.get('page', 1)
        paginator = Paginator(data['businesses'], 12)
        pages = paginator.page_range

        results = paginator.page(results_page)

        print("Suggestions: GET Request")
        context = {'title':'Suggestions',
                   'results':results,
                   'query':'',
                   'location':'Irvine, CA',
                   'time_form': time_form,
                   'pages': pages,
                   }

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/search.html',
            context)

    else:
        return render(request,"app/search.html",{})

@login_required
@require_POST
def vote(request):
    """if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        group = GroupVote.objects.get(name = groupname)

        if company.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            company.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            company.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': company.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    """
    print("hello")

@login_required
def voting(request):
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
        'app/voting.html',
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

@login_required
def user_autocomplete(request):
    if request.is_ajax():
        if 'term' in request.GET:
            print(request.GET)
            q = request.GET.get('term', '')

            print("Querying Database for Users")
            raw_data = CustomUser.objects.all()
            users = []

            for u in raw_data:
                if u.username.startswith(q):
                    users.append(u.username)
            
            data = json.dumps(users)
        else:
            print('term not found!')
    return HttpResponse(data, 'application/json')

def yelp_autocomplete(request):
    if request.is_ajax():
        if 'term' in request.GET:
            print(request.GET)
            q = request.GET.get('term', '').capitalize()

            if cache.get(''.join(i for i in str('autoc-'+q) if i.isalnum())):
                print("Using cached autocomplete results!")
                print(''.join(i for i in str('autoc-'+q) if i.isalnum()))
                data = cache.get(''.join(i for i in str('autoc-'+q) if i.isalnum()))
            else:
                print("Querying Yelp Fusion Autocomplete API")
                raw_data = yelp_api.autocomplete_query(text=q)
                autoc_results = []

                if len(raw_data['terms']) > 0:
                    for t in raw_data['terms']:
                        autoc_results.append(t['text'])
                if len(raw_data['businesses']) > 0:
                    for b in raw_data['businesses']:
                        if c['text']:
                            autoc_results.append(c['text'])
                        elif c['name']:
                            autoc_results.append(c['name'])
                if len(raw_data['categories']) > 0:
                    for c in raw_data['categories']:
                        autoc_results.append(c['title'])
                data = json.dumps(autoc_results)
                cache.set(''.join(i for i in str('autoc-'+q) if i.isalnum()), data, 86400)
        else:
            print('term not found!')
    return HttpResponse(data, 'application/json')