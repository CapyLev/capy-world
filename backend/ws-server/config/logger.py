LOGGING_CONF = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/server.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
}
