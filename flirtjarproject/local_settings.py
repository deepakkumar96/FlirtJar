"""
Django settings for flirtjarproject project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.conf import settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x95+tpnljpc0t2m6j2u+#4k3%o2#u3da@j#dsan#=5&k_%$^*3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'flirtjar.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'accounts',
    'profiles',
    'locations',
    'notifications',
    'chat',

    # Third-Party Apps
    'rest_framework',
    'rest_framework_gis',
    'django_extensions',
    'leaflet',
    'rest_auth',
    'rest_framework_jwt',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_framework_docs',
    # 'debug_toolbar',
    'drf_autodocs',
    'push_notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug
]

ROOT_URLCONF = 'flirtjarproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'flirtjarproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fjdb',
        'USER': 'fjuser',
        'PASSWORD': '12345six',
        'HOST': 'localhost',
        'PORT': '',
}
}

# from accounts.renderer import CustomJSONRenderer

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
         'rest_framework.authentication.TokenAuthentication',
         'rest_framework.authentication.SessionAuthentication',
         # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'accounts.renderer.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

    ),
    'EXCEPTION_HANDLER': 'accounts.util.custom_exception_handler',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserSerializer'
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
AUTH_USER_MODEL = 'custom_auth.Account'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# REST_USE_JWT = True

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': False  # Default: False
}


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
INTERNAL_IPS = ('127.0.0.1',)


def custom_show_toolbar(request):
    return True  # Always show toolbar, for example purposes only.


DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: not request.is_ajax() and request.META.get('REMOTE_ADDR', None) in INTERNAL_IPS,
    'INTERCEPT_REDIRECTS': False,

}


SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },


    # "is_authenticated": True,  # Set to True to enforce user authentication,
    # "is_superuser": False,  # Set to True to enforce admin only access
}

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'accounts.Account'

LEAFLET_CONFIG = {
  'DEFAULT_CENTER': (23.5678, 72.2323),
  'DEFAULT_ZOOM': 12,
  'MIN_ZOOM': 1,
  'MAX_ZOOM': 24,
}


""" Push Notification Settings """

PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": "AAAAX4lHVjs:APA91bEwGJN9QjDIuNOGMTvavq7PEEcbi28Hxxyc2Q-7XUe2jQgYpn-7h47vP13NJ-Wm2x0JJbSJsYRkduVTNd7qq5Br-8qRye_cZHzoWDFLNOGKfAgGBLQwjnQzG5gyex3_x9tNzzeM",
        "FCM_API_KEY": "AAAAX4lHVjs:APA91bEwGJN9QjDIuNOGMTvavq7PEEcbi28Hxxyc2Q-7XUe2jQgYpn-7h47vP13NJ-Wm2x0JJbSJsYRkduVTNd7qq5Br-8qRye_cZHzoWDFLNOGKfAgGBLQwjnQzG5gyex3_x9tNzzeM",
        "APNS_CERTIFICATE": os.path.join(BASE_DIR, 'flirtjarproject/APNSDevelopmentCertificates.pem'),
}
