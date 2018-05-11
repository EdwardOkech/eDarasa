from os import environ
from .base import *
from ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('/home/fraogongi/.app_settings/workstry/settings.ini')

########## SECRET CONFIGURATION
SECRET_KEY = config.get('secrets','SECRET_KEY')

########## HOST CONFIGURATION
ALLOWED_HOSTS = [
    'workstry.com',
    'www.workstry.com',
]
########## END HOST CONFIGURATION


########## STATIC CONFIGURATION
STATIC_URL = 'http://www.workstry.com/static/'
STATIC_ROOT = '/home/fraogongi/webapps/workstry_app_static/'
########## END STATIC CONFIGURATION


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
    },
}
########## END DATABASE CONFIGURATION

########## PESAPAL CONFIGURATION
PESAPAL_DEMO = False
PESAPAL_CONSUMER_KEY = config.get('pesapal','PESAPAL_CONSUMER_KEY')
PESAPAL_CONSUMER_SECRET = config.get('pesapal','PESAPAL_CONSUMER_SECRET')

# Production
PESAPAL_IFRAME_LINK = 'https://www.pesapal.com/api/PostPesapalDirectOrderV4'
PESAPAL_QUERY_STATUS_LINK = 'https://www.pesapal.com/API/QueryPaymentDetails'

PESAPAL_OAUTH_CALLBACK_URL = 'transaction_completed'
PESAPAL_OAUTH_SIGNATURE_METHOD = 'SignatureMethod_HMAC_SHA1'
PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = 'purchase:process_payment_feedback'
PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = 'purchase:process_payment_feedback'
PESAPAL_REDIRECT_WITH_REFERENCE = True
PESAPAL_TRANSACTION_MODEL = 'django_pesapal.Transaction'
########## END PESAPAL CONFIGURATION

WSGI_APPLICATION = 'jm_lms.wsgi_prod.application'

# Since Django has been installed in a directory, we need this here
#FORCE_SCRIPT_NAME = '/d'
