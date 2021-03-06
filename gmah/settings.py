"""
Django settings for gmah project.

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
SECRET_KEY = 'w3_0rp^d^mfv4q+yu$@h@rsht@t1)^gb!y)0uf$^8q--#ovnpd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gmah',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gmah.urls'

WSGI_APPLICATION = 'gmah.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = '/projects/gmah/claim_files/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'claim_files')
MEDIA_ROOT = '/home/hasadimr/domains/hasadim.ru/public_html/media/'
MEDIA_URL = '/media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = 'http://hasadim.ru/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_URL = '/static/'
STATIC_ROOT = '/home/hasadimr/domains/hasadim.ru/public_html/static/'
STATIC_URL = '/static/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s\n",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        # 'null': {
            # 'level': 'DEBUG',
            # 'class': 'django.utils.log.NullHandler',
        # },
        # 'console':{
            # 'level': 'DEBUG',
            # 'class': 'logging.StreamHandler',
            # 'formatter': 'simple'
        # },
        # 'mail_admins': {
            # 'level': 'ERROR',
            # 'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        # }
        'file': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': MEDIA_ROOT + "logfile.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
        # 'django': {
            # 'handlers': ['null'],
            # 'propagate': True,
            # 'level': 'INFO',
        # },
        # 'django.request': {
            # 'handlers': ['mail_admins'],
            # 'level': 'ERROR',
            # 'propagate': False,
        # },
        # 'myproject.custom': {
            # 'handlers': ['console', 'mail_admins'],
            # 'level': 'INFO',
            # 'filters': ['special']
        # }
    }
}