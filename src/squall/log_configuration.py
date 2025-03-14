log_config_dict = {
    "version": 1,
    "loggers": {
        "squall": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "stream_formatter",
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "file_formatter",
            "filename": "squall.log",
        },
    },
    "formatters": {
        "file_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "stream_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
}
