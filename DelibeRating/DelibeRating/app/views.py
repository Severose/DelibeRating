"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About Me',
            'message':'A brief introduction.',
            'year':datetime.now().year,
        }
    )

def login(request):
    """Renders the todo page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        {
            'title':'Login',
            'message':'Login to your account.',
            'year':datetime.now().year,
        }
    )

@login_required
@transaction.atomic
def update_profile(request, user_id):
    """Renders the update_profile page."""
    if request.method == 'POST':
        user_form = UserForm(requiest.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'profiles/profile.html', {
            'title':'Update Profile',
            'message':'Update your account profile.',
            'year':datetime.now().year,
            'user_form': user_form,
            'profile_form': profile_form
        })

def register(request):
    """Renders the register page."""
    if request.method == 'POST':
        user_form = UserAccountForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your account was successfully created!'))
            return redirect('login')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserAccountForm()
        profile_form = ProfileForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/register.html',
        {
            'title':'Register',
            'message':'Register a new user account.',
            'year':datetime.now().year,
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

def todo(request):
    """Renders the todo page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/todo.html',
        {
            'title':'ToDo',
            'message':'This has not been implemented.',
            'year':datetime.now().year,
        }
    )