logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'app_formatter': {
            'format': '[{asctime}] [{levelname}]: {module}:{funcName}:{lineno} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'app_handler': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'filename': 'app.log',
            'mode': 'w',
            'formatter': 'app_formatter',
        },
    },
    'loggers': {
        'app_logger': {
            'level': 'INFO',
            'handlers': ['app_handler'],
        },
    },
}
