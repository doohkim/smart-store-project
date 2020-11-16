from .base import *

# SECRETS_DEV = SECRETS_FULL['dev']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'config.wsgi.dev.application'

# Static files (CSS, JavaScript)
# STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')

ALLOWED_HOSTS += [
    '*',
]

INSTALLED_APPS += [
    'django_extensions',
]

