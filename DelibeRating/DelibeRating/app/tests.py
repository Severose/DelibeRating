"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_settings(self):
        """Tests the settings page."""
        response = self.client.get('/settings')
        self.assertContains(response, 'Settings', 3, 200)

    def test_login(self):
        """Tests the login page."""
        response = self.client.get('/login')
        self.assertContains(response, 'Login', 3, 200)

    def test_register(self):
        """Tests the register page."""
        response = self.client.get('/register')
        self.assertContains(response, 'Register', 3, 200)

    def test_password(self):
        """Tests the register page."""
        response = self.client.get('/password')
        self.assertContains(response, 'Password', 3, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'About', 3, 200)
