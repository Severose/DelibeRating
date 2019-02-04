"""
Definition of forms.
"""

from django import forms
from app.models import *
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

class CustomUserAuthenticationForm(ModelForm):

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
        model = User
        fields = ("username", "password")

class CustomUserCreationForm(ModelForm):

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
 
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        new_user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            #self.cleaned_data['password2'],
            #self.cleaned_data['password2'],
            #self.cleaned_data['password2'],
        )
        return new_user

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'