from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sz^hs)037*^9jkp!s6p3$e@jqz0_k%ee+v%=#t8&gnzpi7mdov'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',  # добавляем адреса доменов.
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',  # добавляем приложение бутстрап для верстки HTML.
    'blog.apps.BlogConfig',  # добавляем приложение блог (основное приложение).
    'pages.apps.PagesConfig',  # добавляем приложение пейджес (приложение статичных страниц).
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

# обозначаем диррикторию для статичных файлов.
STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

ROOT_URLCONF = 'blogicum.urls'

# обозначаем диррикторию шаблонов.
TEMPLATES_DIR = BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'blogicum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# обозначаем язык проекта.
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# прописываем вывод шаблона ошибки 403.
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

# прописываем дирректорию загрузки и ссылку на медиа.
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Указываем адрес для редиректа после авторизации
LOGIN_REDIRECT_URL = 'blog:index'
LOGIN_URL = 'login'

# Подключаем бэкенд filebased.EmailBackend.
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# Указываем директорию, в которую будут сохраняться файлы писем.
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'