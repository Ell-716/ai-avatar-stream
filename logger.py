"""
Centralized logging configuration for the AI Avatar Stream project.

Provides colored console output for development and rotating file logs for production.
All modules should import and use this logger instead of print() statements.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

try:
    import colorlog
    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False


# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Log file configuration
LOG_FILE = os.path.join(LOGS_DIR, "app.log")
MAX_BYTES = 10 * 1024 * 1024  # 10 MB per log file
BACKUP_COUNT = 5  # Keep up to 5 rotated log files


def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger with console and file handlers.

    Args:
        name: Logger name (typically __name__ of the calling module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger_name = name or "ai-avatar-stream"
    logger = logging.getLogger(logger_name)

    # Avoid adding handlers multiple times if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    # ── Console Handler (colored output) ──
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    if HAS_COLORLOG:
        # Colored formatter for development
        console_formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s] [%(levelname)-8s] [%(module)s]%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            reset=True,
            style='%'
        )
    else:
        # Fallback to standard formatter if colorlog not available
        console_formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)-8s] [%(module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # ── File Handler (rotating logs) ──
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Log everything to file

        file_formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)-8s] [%(module)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Failed to set up file handler: {e}")

    return logger


# Create default logger for the application
logger = setup_logger("ai-avatar-stream", level=logging.INFO)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Module name (use __name__)
        level: Logging level

    Returns:
        Logger instance
    """
    return setup_logger(name, level)
