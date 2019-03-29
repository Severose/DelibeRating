from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

with open(os.environ.get('prod')) as f:
    configs = json.loads(f.read())

def get_env_var(setting, configs=configs):
 try:
     val = configs[setting]
     if val == 'True':
         val = True
     elif val == 'False':
         val = False
     return val
 except KeyError:
     error_msg = "ImproperlyConfigured: Set {0} environment      variable".format(setting)
     raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var("SECRET_KEY")
DB_NAME = get_env_var("DB_NAME")
DB_USER = get_env_var("DB_USER")
DB_PASS = get_env_var("DB_PASS")

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASS',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}