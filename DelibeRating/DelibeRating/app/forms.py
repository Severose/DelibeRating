"""
Definition of forms.
"""

from django import forms
from app.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _

class CustomUserAuthenticationForm(AuthenticationForm):

    username = forms.CharField(label='Username', min_length=4, max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        return username
 
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        #if
        return password

    class Meta:
        model = CustomUser
        fields = ("username", "password")

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))

    email = forms.EmailField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'A valid email address'}))

    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    password2 = forms.CharField(label=_("Password Confirmation"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password confirmation'}))

    first_name = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'First name'}))

    last_name = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Last name'}))

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

    def cleaned_data(self):
        # Get username
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")

        # Get password
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        # Get email
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")

        # Get first and last names
        first_name = self.cleaned_data['first_name'].lower()
        last_name = self.cleaned_data['last_name'].lower()

        # Combine all user data
        return {
            'username':   username,
            'password2':  password2,
            'email':      email,
            'first_name': first_name,
            'last_name': last_name,}


    def save(self, commit=True):
        new_user = CustomUser.objects.create_user(
            clean_username('username'),
            clean_password2('password2'),
            clean_email('email'),
            clean_firstname('first_name'),
            clean_lastname('last_name'),
        )
        return new_user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password", "email", "first_name", "last_name")
