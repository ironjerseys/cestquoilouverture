from .base import *
import os

SECRET_KEY = os.getenv('SECRETKEY')

DEBUG = 'True'

ALLOWED_HOSTS = [
    'cestquoilouverture.com',
    'www.cestquoilouverture.com',
    'https://cestquoilouverture.com/',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ironjerseys_cestquoilouverture',
        'USER': os.getenv('DBUSER'),
        'PASSWORD': os.getenv('DBPASSWORD'),
        'HOST': 'postgresql-ironjerseys.alwaysdata.net',
        'PORT': '5432',
    }
}