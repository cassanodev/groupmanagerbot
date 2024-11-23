"""
Logger Module

This module provides logging functionality for the Telegram bot.
It configures logging to both file and console output, enabling:
- Debug and error tracking
- Operation monitoring
- System status logging

The logger is configured to provide detailed information about
bot operations and any issues that arise during execution.
"""

import logging

# Configure basic logging settings
logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    This function returns a logger configured with the basic settings
    defined above. The logger will output messages to both a file
    and the console.

    Args:
        name (str): The name for the logger, typically __name__
                   of the calling module

    Returns:
        logging.Logger: Configured logger instance
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Bot started")
        2024-01-01 12:00:00 - module_name - INFO - Bot started
    """
    return logging.getLogger(name)
