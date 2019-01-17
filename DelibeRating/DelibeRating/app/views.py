"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

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
            'title':'About Us',
            'message':'\'Us\' is more of \'I\', actually...',
            'year':datetime.now().year,
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