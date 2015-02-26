# -*- coding:utf-8 -*-
"""
Django settings for CP4 project.

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
SECRET_KEY = 'enshuesz6v_p_9ig4h&ci&94+1tp&($rom+2%x$nr@+u^&r!!j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    # templates文件夹的路径(模板所在路径)
    # os.path.dirname(__file__)获取当前文件所在的绝对路径(settings.py文件)
    # os.pardir获取上一层目录
    # os.path.join 这个方法将这目录与 templates 进行连接。如果在windows下，它会智能地选择正确的后向斜杠”“进行连接，而不是前向斜杠”/”。

    os.path.join(BASE_DIR,'templates').replace('\\','/'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HomePage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CP4Reporter.urls'

WSGI_APPLICATION = 'CP4Reporter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'mysite',
        'USER':'root',
        'PASSWORD':'admin',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # 静态文件地址
    os.path.join(BASE_DIR,'static').replace('\\','/'),
)