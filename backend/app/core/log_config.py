import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from loguru import logger

from app.core.variables import SettingLogging


def setup_logger() -> Any:
    """Настройка логгера с использованием loguru."""
    app_logger = logger.bind(app='vink')

    for logger_name in SettingLogging.SUPPRESSED_LOGGERS:
        app_logger.disable(logger_name)

    os.makedirs(SettingLogging.LOG_DIR, exist_ok=True)

    log_file = Path(SettingLogging.LOG_DIR) / \
        f'app_{datetime.now().strftime(SettingLogging.LOG_DATE_FORMAT)}.log'
    app_logger.add(
        sink=log_file,
        rotation=SettingLogging.LOG_ROTATION,
        retention=SettingLogging.LOG_RETENTION,
        encoding=SettingLogging.LOG_FILE_ENCODING,
        format=SettingLogging.LOG_FORMAT,
        level=SettingLogging.LOG_LEVEL,
        compression=SettingLogging.LOG_COMPRESSION,
        enqueue=False,
    )
    app_logger.configure(extra={'endpoint': 'system', 'method': 'N/A'})
    return app_logger


def log_action_status(
    error: Optional[Exception] = None,
    action_name: str = 'Action',
    message: str = '',
) -> None:
    """Логирует ошибку при выполнении произвольного действия."""
    if error is not None:
        exc_tb = sys.exc_info()[-1]
        last_frame = traceback.extract_tb(exc_tb)[-1] if exc_tb else None

        app_logger.opt(depth=1).error(
            f'{action_name} FAILED | '
            f'Error: {str(error)} | '
            f'Location: {last_frame.filename if last_frame else 'unknown'} | '
            f'String: {last_frame.lineno if last_frame else 'unknown'} | '
            f'Function: {last_frame.name if last_frame else 'unknown'}',
        )
    else:
        app_logger.info(message)


app_logger = setup_logger()
