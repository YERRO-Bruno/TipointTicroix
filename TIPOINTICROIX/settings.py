"""
Django settings for TIPOINTICROIX project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
print(DEBUG)

ALLOWED_HOSTS = ['192.168.1.188', 'localhost', '127.0.0.1',"*","tipointticroix-tipointticroix.*",'195.35.28.193']
CSRF_TRUSTED_ORIGINS = ['https://tipointticroix-tipointticroix.zd04p4.easypanel.host',
                        "https://195.35.28.193","https://tipointticroix.fr"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tipoint_ticroix.apps.TipointTicroixConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TIPOINTICROIX.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TIPOINTICROIX.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
import mysql.connector
DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": os.getenv('NAME'),
        "USER": os.getenv('USER'),
        "PASSWORD": os.getenv('PASSWORD'),
        "HOST": os.getenv('HOST'),
        'PORT': 3306,  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }  
}  
AUTH_USER_MODEL = 'tipoint_ticroix.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
os.path.join(BASE_DIR, "tipoint_ticroix/static")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# Django Emails
DEBUG_EMAIL = os.getenv('DEBUG_EMAIL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

#GOODIES - Pjotos


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TOUR=0
BEGIN=""
NIVEAU=0
NIVEAU1=0
NIVEAU2=0
MODEJEU=""
MARQUEORDI=""
MARQUEJOUEUR=""
COUPJOUEUR=""
COUPORDINATEUR=""
EMAIL=""
GRILLE = [["-"] * 25 for _ in range(25)]
SEQUENCE = []
MATCH=0
MYIP=""
IPSERVEUR=""
BEGINCLIENT=""
BEGINSERVEUR=""
PREMIER=""
SECOND=""
NOMSERVEUR=""
NOMCLIENT=""
SOCKETSERVEUR=""
SOCKETCLIENT=""
MARQUESERVEUR=""
MARQQUECLIENT=""
SCORE1=0
SCORE2=0