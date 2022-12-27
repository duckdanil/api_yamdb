import os

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reviews.apps.ReviewsConfig',
    'api.apps.ApiConfig',
    'rest_framework',
#    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_yamdb.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'api_yamdb.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = ((BASE_DIR / 'static/'),)

AUTH_USER_MODEL = 'reviews.User'

# Минимальная оценка произведения
MIN_SCORE = 1
MIN_SCORE_MESSAGE = f'Минимальная оценка {MIN_SCORE}!'
# Максимальная оценка произведения
MAX_SCORE = 10
MAX_SCORE_MESSAGE = f'Максимальная оценка {MAX_SCORE}!'
# Максимальная длина адреса электронной почты
MAX_LENGTH_EMAIL = 254
# Максимальная длина username
MAX_LENGTH_USERNAME = 150
# Минимальный год издания произведения
MIN_YEAR_TITLE = 1
SMALL_YEAR_MESSAGE = 'Год не должен быть меньше {MIN_YEAR_TITLE}'
BIG_YEAR_MESSAGE = 'Указать год из будущего не получится!'
# Email
load_dotenv()
# SMTP backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Backend для эмуляции почтового сервера
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# Директория для писем при эмуляции
#EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
CONFIRMATION_CODE_LENGTH = 64

# Работа с токенами
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ]
# }
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }
