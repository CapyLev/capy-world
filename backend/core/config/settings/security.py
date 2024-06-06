from .constants import application_consts

SECRET_KEY = application_consts.server.SECRET_KEY
DEBUG = application_consts.server.DEBUG
ALLOWED_HOSTS = application_consts.server.ALLOWED_HOSTS

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CORS_ALLOW_CREDENTIALS = application_consts.server.CORS_ALLOW_CREDENTIALS
CORS_ALLOWED_ORIGINS = application_consts.server.CORS_ALLOWED_ORIGINS

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]
