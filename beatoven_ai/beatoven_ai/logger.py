"""
Logging configuration for the beatoven_ai package.
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "beatoven_ai",
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure and return a logger with the specified settings.

    Args:
        name: Logger name
        log_level: Logging level (default: INFO)
        log_file: Path to log file (optional)
        console: Whether to log to console (default: True)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Remove existing handlers to avoid duplicate logging
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Add file handler if requested
    if log_file:
        log_path = Path(log_file).resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


# Default logger instance
logger = setup_logger()