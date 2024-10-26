from pathlib import Path
import os
from decouple import config
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=4ip=kp_r#mxvtnph26h=6jl9#k011@v*@o-64=r2bj%d@fx6p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.MyUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'tinymce',
    "crispy_forms",
    "crispy_bootstrap5",
    'blog',
    'recettes',
    'contact',
    'django_recaptcha',
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# TINYMCE_DEFAULT_CONFIG = {
#     'height': 360,
#     'width': 900,
#     'cleanup_on_startup': True,
#     'custom_undo_redo_levels': 20,
#     'selector': 'textarea',
#     'plugins': 'paste',
#     'paste_as_text': True,
#     'toolbar': 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat',
# }


DEFAULT_CONFIG = getattr(
    settings,
    "TINYMCE_DEFAULT_CONFIG",
    {
        "theme": "silver",
        "height": 500,
        "menubar": False,
        "browser_spellcheck": True,
        "plugins": "advlist,autolink,lists,link,image,charmap,preview,anchor,"
        "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,"
        "help,wordcount",
        "toolbar": "undo redo | formatselect | "
        "bold italic backcolor | alignleft aligncenter "
        "alignright alignjustify | bullist numlist outdent indent | "
        "removeformat | help",
    },
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cuisineantillaise.urls'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s" 
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'cuisineantillaise.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME' : config('DB_NAME'),
        'USER' : config('DB_USER'),
        'PASSWORD' : config('DB_PASSWORD'),
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}

RECAPTCHA_PUBLIC_KEY = config('CAPTCHA_PUBLIC')
RECAPTCHA_PRIVATE_KEY = config('CAPTCHA_PRIVATE')



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


USE_REMEMBER_ME = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'david.accipe@gmail.com'
EMAIL_HOST_PASSWORD = 'xxoy avhg dwzx kesv'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIR = [BASE_DIR, 'static']
STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static"),
                    ]
MEDIA_URL = 'media/'
# MEDIA_ROOT = [BASE_DIR, 'mediafiles']
# MEDIA_ROOT = [ os.path.join(BASE_DIR, "mediafiles")]
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# TINYMCE_JS_ROOT = os.path.join(MEDIA_URL, "path/to/tinymce")
# TINYMCE_COMPRESSOR = True

USE_COMPRESSOR = getattr(settings, "TINYMCE_COMPRESSOR", False)

USE_EXTRA_MEDIA = getattr(settings, "TINYMCE_EXTRA_MEDIA", None)

USE_FILEBROWSER = getattr(
    settings, "TINYMCE_FILEBROWSER", "filebrowser" in settings.INSTALLED_APPS
)

def get_js_url():
    return getattr(
        settings,
        "TINYMCE_JS_URL",
        staticfiles_storage.url("tinymce/tinymce.min.js"),
    )