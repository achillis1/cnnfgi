import os, django, sys

DJANGO_ENV = os.environ.get('DJANGO_ENV') or 'development'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
if DJANGO_ENV == 'production':
    BASE_URL = 'cnnfgi.herokuapp.com'
    PROTOCOL = 'http'
elif DJANGO_ENV == 'staging':
    BASE_URL = 'cnnfgi-staging.herokuapp.com'
    PROTOCOL = 'http'
else:
    BASE_URL = '127.0.0.1:8000'
    PROTOCOL = 'http'

ADMINS = (
    ('Ding Li',     'dli@nexant.com'),
)

if DJANGO_ENV == 'development':
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage' #need S3 for file_upload function
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # Always use S3 on staging/production
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_PRELOAD_METADATA = True

PHANTOMJS_PATH = os.environ.get('LD_LIBRARY_PATH')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if DJANGO_ENV == 'development':
    # Won't generally collect locally, but if we do, collect to here
    STATIC_ROOT = '%s/staticfiles/' % SITE_ROOT
else:
    STATIC_ROOT = '%s/staticfiles/' % SITE_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# STATIC_URL = '/static/'
if DJANGO_ENV == 'development':
    # Use this to at least pull css/js/etc. from local folder when no internet available
# STATIC_URL = '/static/'

    #otherwise
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
else:
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'fqpysz9gg@-(4oerhmb9p&2-vlf6no4_xazvm6s^+3=f3h8rg='

if DJANGO_ENV == 'production':
    DEBUG = False
else:
    DEBUG = True


if DJANGO_ENV in ['development', 'staging']:
    ALLOWED_HOSTS = ['.cnnfgi-staging.herokuapp.com',
                     '127.0.0.1',
                     ]
else:
    ALLOWED_HOSTS = ['.cnnfgi.herokuapp.com',
                     ]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'cnnfgiapp',
    'storages',
    'django.contrib.humanize',
    'haystack',
    'sphinxdoc',
    'axes',
    'reversion',
    'crispy_forms',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'simple_history.middleware.HistoryRequestMiddleware',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_API_KEY = os.environ.get('EMAIL_API_KEY')

# Mail configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'dingli@gmail.com'
DEFAULT_FROM_EMAIL = 'dingli@gmail.com'
EMAIL_TEMPLATE = os.environ.get('EMAIL_TEMPLATE') or 'sample-template'
if DJANGO_ENV == 'development':
  EMAIL_HOST = 'smtp.sendgrid.net'
  EMAIL_PORT = 587
  EMAIL_HOST_USER = EMAIL_USERNAME
  EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
  EMAIL_PROVIDER = 'sendgrid'
else:
  EMAIL_HOST = 'smtp.sendgrid.net'
  EMAIL_PORT = 587
  EMAIL_HOST_USER = EMAIL_USERNAME
  EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
  EMAIL_PROVIDER = 'sendgrid'

ROOT_URLCONF = 'cnnfgi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'cnnfgitemplates')],
        #'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders':[
                ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
                )),
            ],

        },
    },
]


WSGI_APPLICATION = 'cnnfgi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
if DJANGO_ENV == 'development':
    NAME = os.environ.get('NAME')
    ENGINE = os.environ.get('ENGINE')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    DATABASES = {'default': {
                    'ENGINE': ENGINE,
                    'NAME': NAME,
                    'USER': USER,
                    'PASSWORD': PASSWORD,
                    'HOST': HOST,
                    'PORT': PORT},}
else:
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] =  dj_database_url.config()


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/login/'

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'US/Eastern'
TIME_ZONE = 'US/Central'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CRISPY_FAIL_SILENTLY = not DEBUG
