"""
Bot Middleware Module

This module implements middleware functionality for the Telegram bot.
The middleware processes incoming updates before they reach handlers,
performing tasks such as:
- User verification
- Update filtering
- Pre-processing of messages and callbacks
"""

from telebot import asyncio_handler_backends
from utils.user import check_user

class Middleware(asyncio_handler_backends.BaseMiddleware):
    """
    Custom middleware for processing bot updates.

    This middleware handles pre-processing of messages and callback queries,
    ensuring that user data is properly initialized before updates are processed
    by handlers.

    Attributes:
        update_types (list): List of update types this middleware processes
    """

    def __init__(self):
        """
        Initialize the middleware.

        Sets up the update types that this middleware will process:
        - messages
        - callback queries
        """
        self.update_types = ['message', 'callback_query']

    async def pre_process(self, message, data):
        """
        Process updates before they reach handlers.

        This method ensures that user data exists in the database
        for any user interacting with the bot.

        Args:
            message: The incoming update (message or callback query)
            data: Additional data passed through middleware chain
        """
        await check_user(message)

    async def post_process(self, message, data, exception):
        """
        Process updates after they've been handled.

        Currently implemented as a pass-through, but can be extended
        to handle post-processing tasks or error handling.

        Args:
            message: The processed update
            data: Additional data from middleware chain
            exception: Any exception that occurred during handling
        """
        pass
