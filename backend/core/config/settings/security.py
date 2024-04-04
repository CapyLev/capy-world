from .constants import application_consts

SECRET_KEY = application_consts.server.SECRET_KEY

DEBUG = application_consts.server.DEBUG

ALLOWED_HOSTS = application_consts.server.ALLOWED_HOSTS

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.account.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.account.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.account.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.account.password_validation.NumericPasswordValidator",
    },
]
