DEBUG = False

SECRET_KEY = ''

# Admin e-mail addresses to send messages to when errors occur
ADMINS = ['admins@sfi.pl']

ALLOWED_HOSTS = ['warsztaty.sfi.pl']

STATIC_ROOT = '/var/www/enroll/static'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'enroll',
        'USER': 'enroll',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'disable'
        },
    }
}

EMAIL_HOST = '10.20.0.101'
EMAIL_PORT = 25

OIDC_RP_CLIENT_ID = 'enroll'
OIDC_RP_CLIENT_SECRET = ''
