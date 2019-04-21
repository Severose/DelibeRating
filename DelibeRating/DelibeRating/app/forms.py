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
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               label='Username')
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Password')

    class Meta:
        model = CustomUser
        fields = ("username", "password")

class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form for the CustomUser model
        username, password1, password2, email, first_name, last_name
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                               label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)'}),
                               label='Password confirmation')
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                               label='Email')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}),
                               label='First name', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
                               label='Last name', required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    """Custom User Change Form for the CustomUser model
        username, password, email, first_name, last_name
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               label='Username', required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                               label='Email', required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}),
                               label='First name', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
                               label='Last name', required=False)

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
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                               label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)'}),
                               label='Password confirmation')

    class Meta:
        model = CustomUser
        fields = ("password1", "password2")
