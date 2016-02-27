"""
Django settings for studentsdb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .db import DATABASES

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
os.path.join(BASE_DIR, 'studentsdb', 'templates'),
)

from django.conf import global_settings

TEMPLATE_CONTEXT_PROCESSORS = \
    global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "studentsdb.context_processors.students_proc",
    "students.context_processors.groups_processor",
    )
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '737s0%6epg_m5b4o%(!$ct692$2o&v=9bep4aqh1!en#6hc4-='

SOCIAL_AUTH_FACEBOOK_SECRET = '5bc25ad5e42ac9ff449571a067775bb5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

REGISTRATION_OPEN = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'registration',
    'social.apps.django_app.default',
    'students',
    'studentsdb',
)

MIDDLEWARE_CLASSES = (
    'studentsdb.middleware.RequestTimeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')


PORTAL_URL = 'http://localhost:8000'

# email settings

ADMIN_EMAIL = ''
EMAIL_HOST = ''
EMAIL_PORT = '587'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'students.views.contact_admin': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}

AUTHENTICATION_BACKENDS = (
'social.backends.facebook.FacebookOAuth2',
'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1267619993255398'