"""
Django settings for djangoproj project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jjgbf!dkb2ym)06rj8w)5u2kc@*(6y8gw#2123=si&wy&fpkt&'

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRON = os.environ.get('ENVIRONMENT', 'PRODUCTION')
DEBUG = False
if ENVIRON == 'DEVELOPMENT':
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Local Apps (Your project's apps)
    'app',

    # Third-Party Apps
    'corsheaders',
    'rest_framework',
    'rest_framework_gis',
    # for authentication
    'rest_framework.authtoken',
    'rest_auth',
    # for registration
    'django.contrib.sites',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount'

]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'app.permissions.IsOwnerOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # for browsable api view usage
        'rest_framework.authentication.SessionAuthentication',
        # enables simple command line authentication
        'rest_framework.authentication.BasicAuthentication',
    ),

    # 'PAGINATE_BY': 100,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'app.renderers.BrowsableAPIRendererWithoutForms',
    ),
}

# Enables django-rest-auth to use JWT tokens instead of regular tokens.
REST_USE_JWT = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=4)
}

SITE_ID = 1

# Django allauth (account registration email flow)

ACCOUNT_ADAPTER = 'app.adapter.MyAccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Bicultural Tool] "

# To be able to login after putting in place the registration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend"
]

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'app.serializers.CustomPasswordResetSerializer'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Allow CORS
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'djangoproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app', 'templates')],
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

WSGI_APPLICATION = 'djangoproj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

db_user = os.environ.get('POSTGRES_USER', 'mapuser')
db_pass = os.environ.get('POSTGRES_PASSWORD', 'password')
db_name = os.environ.get('POSTGRES_DB', db_user)
db_host = os.environ.get('POSTGRES_HOSTNAME', 'localhost')
db_port = os.environ.get('POSTGRES_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_pass,
        'HOST': db_host,
        'PORT': db_port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/staticfiles/'

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_MAX_MEMORY_SIZE = 1000000000
DATA_UPLOAD_MAX_MEMORY_SIZE = 1000000000
FILE_UPLOAD_PERMISSIONS=0o644

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'geospatial.rotorua@gmail.com'
email_pass = os.environ.get('EMAIL_PASS')
EMAIL_HOST_PASSWORD = email_pass


# Local time zone
TIME_ZONE = "UTC"
USE_TZ = True
USE_I18N = True
USE_L10N = True
