class SettingFieldDB:
    MAX_LENGTH_TITLE = 255
    MAX_SIZE_PAGINATION = 50
    DEFAULT_SIZE_PAGINATION = 5


class SettingLogging:
    SUPPRESSED_LOGGERS: list[str] = ['uvicorn', 'uvicorn.error',
                                     'fastapi', 'uvicorn.access']
    LOG_DIR: str = 'logs'
    LOG_FORMAT: str = (
        '{time:HH:mm:ss} | {level} | {extra[endpoint]} | {message}')
    LOG_DATE_FORMAT: str = '%Y-%m-%d'
    LOG_FILE_ENCODING: str = 'utf-8'
    LOG_ROTATION: str = '00:00'
    LOG_RETENTION: str = '7 days'
    LOG_COMPRESSION: str = 'zip'
    LOG_LEVEL: str = 'DEBUG'
