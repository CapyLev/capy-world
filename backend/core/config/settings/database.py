from .constants import application_consts

DATABASES = {
    'default': {
        'ENGINE': application_consts.database.ENGINE,
        "NAME": application_consts.database.DB_NAME,
        "USER": application_consts.database.DB_USER,
        "PASSWORD": application_consts.database.DB_PASSWORD,
        "HOST": application_consts.database.DB_HOST,
        "PORT": application_consts.database.DB_PORT,
    }
}
