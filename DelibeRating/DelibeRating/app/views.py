"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('contact')
    else:
        form = ContactForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
            'form':ContactForm,
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
    """Renders the login page."""
    print("Login View")
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

def register(request):
    """Renders the register page."""
    print("Register View")
    print(request)
    if request.method == 'POST':
        print("POST Request")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form Valid... Saving")
            form.save()
            #("username", "password", "email", "first_name", "last_name")
            username = CustomUserCreationForm('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            messages.success(request, 'Your account was successfully created!')
            return redirect('index')
        else:
            print("Error: Form Invalid")
            messages.error(request, 'Please correct the error below.')
    else:
        print("GET Request")
        form = CustomUserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/register.html',
        {
            'title':'Register',
            'message':'Register a new user account.',
            'year':datetime.now().year,
            'form':CustomUserCreationForm
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