"""
Logging configuration for Jarvis Mark III
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logger(config: dict) -> logging.Logger:
    """
    Setup rotating file logger with console output.
    
    Args:
        config: Logging configuration from config.yaml
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("jarvis")
    logger.setLevel(getattr(logging, config['level']))
    
    # Ensure log directory exists
    log_file = Path(config['file'])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=config['max_size'],
        backupCount=config['backup_count'],
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
