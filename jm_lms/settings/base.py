# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
                       '@dd2=$x4axk406zp0$$ging9s@w40p*-#_2@ke8imu3v5&07+j')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party apps.
    #'django_extensions',
    'django_summernote',
    'rest_framework',
    'django_pesapal',
    # 'django_social_share',
    
    # Quiz apps
    "jm_lms.apps.quiz",

    # Project apps.
    'jm_lms.apps.homesite',
    'jm_lms.apps.accountusers',
    'jm_lms.apps.courses',
    'jm_lms.apps.dashboard',
    'jm_lms.apps.jobs',
    'jm_lms.apps.registrations',
    'jm_lms.apps.exercises',
    'jm_lms.apps.purchase',
    'jm_lms.apps.askaquestion',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'jm_lms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'jm_lms.wsgi.application'

# """AUTHENTICATION_BACKENDS = (
#     'social.backends.facebook.FacebookOAuth2',
#     'social.backends.google.GoogleOAuth2',
#     'social.backends.twitter.TwitterOAuth',
#     'django.contrib.auth.backends.ModelBackend',
# )"""

# client IDs for social sites
# SOCIAL_AUTH_FACEBOOK_KEY =
# SOCIAL_AUTH_FACEBOOK_SECRET =
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =
# SOCIAL_AUTH_TWITTER_KEY =
# SOCIAL_AUTH_TWITTER_SECRET =


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         # 'NAME': os.getenv('DATABASE_NAME', 'project_name'),
#         # 'USER': os.getenv('DATABASE_USER', 'project_name'),
#         # 'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
#         # 'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
#         # 'PORT': os.getenv('DATABASE_PORT', '5432'),
#
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'some_db',
        'USER': 'some_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'Info <info@example.com>'
SERVER_EMAIL = 'Alerts <alerts@example.com>'

ADMINS = (
    ('Admin', 'fraogongi@gmail.com'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', ],
            'level': 'INFO',
        }
    }
}

# ======================= OVERRIDES ===========================================

# Overriding the default user model
AUTH_USER_MODEL = 'accountusers.AuthUser'

# Set the login url
from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')

SITE_NAME = "Workstry"
SITE_URL = "www.workstry.com"
DEFAULT_FROM_EMAIL = 'info@workstry.com'
EMAIL_SUBJECT_PREFIX = "[Workstry] "



