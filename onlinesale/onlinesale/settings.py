"""
Django settings for onlinesale project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.path.abspath(__file__) = C:\Marker\onlinesale\onlinesale\settings.py
# os.path.dirname(os.path.abspath(__file__)) = C:\Marker\onlinesale\onlinesale\
# os.path.dirname(os.path.dirname(os.path.abspath(__file__))) = C:\Marker\onlinesale\

# So Our Base Directory is :
# BASE_DIR = C:\Marker\onlinesale\


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nu0x)$p3g_^lpd^m_rwcm6co(!4ow)($-4)zf7y$5krr8zu!jm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.User'
# Django allows you to override the default user model by providing a value for the 'AUTH_USER_MODEL' setting that references a custom model

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'carts.apps.CartsConfig',
    'search.apps.SearchConfig',
    'tags.apps.TagsConfig',
    'orders.apps.OrdersConfig',
    'billing.apps.BillingConfig',
    'addresses.apps.AddressesConfig',
    'actors.apps.ActorsConfig',
    'profiles.apps.ProfilesConfig',
    'blog.apps.BlogConfig',
    'coments.apps.ComentsConfig',
    'watchlists.apps.WatchlistsConfig',
    'rest_framework',
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

ROOT_URLCONF = 'onlinesale.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.views.get_genre',
            ],
        },
    },
]

WSGI_APPLICATION = 'onlinesale.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/' #this value could be anything
#this is the public url ( like a pseudo name ) to our directory
#by default django looks for static files in app just like the case in templates 

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static_proj')]
# this is the additional path we are specifying for django to look for static files
# i.e inside our base directory itself

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"replica_static","static_root")
# this specifies where to store all the static files 
# i.e here we storing the static files outside our base directory

# The absolute path to the directory where collectstatic will collect static files for deployment.

MEDIA_URL = "/media/" #this value could be anything
# this is the public url ( like a pseudo name ) to our directory

# this is for the users to upload images

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR),"replica_static","media_root")
# here we are defining the full path to a directory where we like our django 
# to upload the files : in short MEDIA_ROOT is the directory where the uploaded files will be saved

# using the os.path.join method we are making sure that the full path to that directory
# is created correctly no matter what operating system we are on

# for performance reason these files are stored on the file system
# and not on the database

LOGIN_URL = 'signin'

CRISPY_TEMPLATE_PACK = 'bootstrap4'