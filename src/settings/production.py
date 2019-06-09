from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (ROOT_DIR('static'), )

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = env('INTERNAL_IPS')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Boise'
USE_I18N = True
USE_L10N = True
USE_TZ = True
