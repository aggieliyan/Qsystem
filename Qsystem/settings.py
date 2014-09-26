"""
Django settings for Qsystem project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3oc$^^dt!@ir9)-l27(c3qk10w1=knk$1o7z(w48j30!d)(m0('

# SECURITY WARNING: don't run with debug turned on in production!
import socket

if socket.gethostname() == 'test':
    DEBUG = TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['*']
    STATIC_ROOT = '/Django/Qsystem/Qsystem/project/static'
    INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project',
    'south',
)
    
else:
    DEBUG = TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
    INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project',
)

# Application definition


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Qsystem.urls'

WSGI_APPLICATION = 'Qsystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if socket.gethostname() == 'test':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'qsystem',
            'USER':'root',
            'PASSWORD':'mysqlpwd1',
            'HOST':'localhost',
            'PORT':'3306',
                },
        'ajaxableskydb': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ajaxableskydb',
                'USER':'qa',
                'PASSWORD':'as-qa',
                'HOST':'192.168.3.91',
                'PORT':'3306',
             },
        'ablesky_examsystem': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ablesky_examsystem',
                'USER':'qa',
                'PASSWORD':'as-qa',
                'HOST':'192.168.3.91',
                'PORT':'3306',                      
                 },
                }          
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'qsystem',
            'USER':'root',
            'PASSWORD':'mysqlpwd1',
            'HOST':'localhost',
            'PORT':'3306',
                },
        'ajaxableskydb': {           
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ajaxableskydb',
            'USER':'root',
            'PASSWORD':'mysqlpwd1',
            'HOST':'192.168.120.201',
            'PORT':'3306',
                },   
        'ablesky_examsystem': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ablesky_examsystem',
                'USER':'root',
                'PASSWORD':'mysqlpwd1',
                'HOST':'192.168.120.201',
                'PORT':'3306',                      
                 },    
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
