import os
import environ

ROOT_DIR = environ.Path(os.path.abspath('')) - 1  # (src/settings/base.py - 3 = src/)
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    INTERNAL_IPS=(list, []),
)
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = ROOT_DIR()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
