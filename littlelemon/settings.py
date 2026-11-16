import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or secrets.token_urlsafe(50)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'rest_framework.authtoken', 'djoser', 'django_filters', 'restaurant',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'littlelemon.urls'
WSGI_APPLICATION = 'littlelemon.wsgi.application'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates', 'DIRS':[], 'APP_DIRS':True,
              'OPTIONS':{'context_processors':['django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
DATABASES = {'default': {
    'ENGINE':'django.db.backends.mysql',
    'NAME':os.environ.get('MYSQL_DATABASE','littlelemon_capstone'),
    'USER':os.environ.get('MYSQL_USER','littlelemon'),
    'PASSWORD':os.environ.get('MYSQL_PASSWORD',''),
    'HOST':os.environ.get('MYSQL_HOST','127.0.0.1'),
    'PORT':os.environ.get('MYSQL_PORT','3306'),
    'OPTIONS':{'charset':'utf8mb4','init_command':"SET sql_mode='STRICT_TRANS_TABLES'"},
}}
if os.environ.get('DJANGO_USE_SQLITE') == '1':
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 'NAME':BASE_DIR/'db.sqlite3'}}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.TokenAuthentication','rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE':10,
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter'],
}
DJOSER = {'USER_CREATE_PASSWORD_RETYPE':True}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'staticfiles'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
