from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

with open(os.path.join(BASE_DIR, 'settings/dev.json')) as settings_vars_file:
    settings_vars = json.load(settings_vars_file)

def get_var(setting, vars=settings_vars):
    """Get setting or fail with ImproperlyConfigured"""
    try:
        return vars[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_var("SECRET_KEY")
DB_NAME = get_var("DB_NAME")
DB_USER = get_var("DB_USER")
DB_PASS = get_var("DB_PASS")
API_KEY = get_var("API_KEY")

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

settings.configure()