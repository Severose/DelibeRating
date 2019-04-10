"""
Definition of forms.
"""

from django import forms
from app.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

class CustomUserAuthenticationForm(AuthenticationForm):
    """Custom User Authentication Form for the CustomUser model:
        username, password
    """

    class Meta:
        model = CustomUser
        fields = ("username", "password")

class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form for the CustomUser model
        username, password1, password2, email, first_name, last_name
    """
    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    """Custom User Change Form for the CustomUser model
        username, password, email, first_name, last_name
    """
    #username = forms.CharField(initial=user.username)
    #email = forms.CharField(initial=user.email)
    #first_name = forms.CharField(initial=user.first_name)
    #last_name = forms.CharField(initial=user.last_name)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom Password Change Form for the CustomUser model
        password1, password2
    """
    class Meta:
        model = CustomUser
        fields = ("password1", "password2")
