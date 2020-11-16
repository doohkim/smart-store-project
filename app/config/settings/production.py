from .base import *
# SECRETS_DEV = SECRETS_FULL['dev']
DEBUG = False
print(DEBUG)
WSGI_APPLICATION = 'config.wsgi.production.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ALLOWED_HOSTS += ['*']