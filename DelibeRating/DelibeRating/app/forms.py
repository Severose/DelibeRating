"""
Definition of forms.
"""

from django import forms
from app.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _

class CustomUserAuthenticationForm(AuthenticationForm):

    username = forms.CharField(label='Username', min_length=4, max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        # Get username
        username = self.cleaned_data['username'].lower()
        password = self.cleaned_data.get('password')
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ("username", "password")

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(label='Username', min_length=4, max_length=254)
    email = forms.CharField(label='Email', max_length=254)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=254)
    password2 = forms.CharField(label='Password (confirm)', widget=forms.PasswordInput, max_length=254)
    first_name = forms.CharField(label='First name', max_length=254)
    last_name = forms.CharField(label='Last name', max_length=254)

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")
        field_classes = {"username": forms.CharField,
                         "password1": forms.CharField,
                         "password2": forms.CharField,
                         "email": forms.EmailField,
                         "first_name": forms.CharField,
                         "last_name": forms.CharField}

    def clean(self):
        cleaned_data = super().clean()

        # Get username
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")

        # Get password
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
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
        return cleaned_data

    def save(self, commit=True):
        new_user = super(CustomUserCreationForm, self).save(commit=False)
        #new_user = CustomUser.objects.create_user(
        new_user.username = clean_username('username')
        new_user.password = clean_password2('password2')
        new_user.email = clean_email('email')
        new_user.first_name = clean_firstname('first_name')
        new_user.last_name = clean_lastname('last_name')
        print(new_user)
        if commit:
            new_user.save()
        return new_user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password", "email", "first_name", "last_name")
