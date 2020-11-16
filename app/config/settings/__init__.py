import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
print(SETTINGS_MODULE)
if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings':
    from .dev import *

# if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings':
#     from .dev import *
# else:
#     from .production import *