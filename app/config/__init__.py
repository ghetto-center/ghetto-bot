from logging import config as logging_config

from .app_config import config

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s][%(levelname)s][%(funcName)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {},
    "root": {
        "handlers": [
            "console"
        ],
        "level": config.get('LOG_LEVEL', 'DEBUG')
    }
}

# init logging config
logging_config.dictConfig(config.get('logging', DEFAULT_LOGGING))
