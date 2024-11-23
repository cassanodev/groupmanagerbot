"""
Bot Instance Module

This module handles the initialization and setup of the Telegram bot instance including:
- Bot configuration
- Middleware setup
- Handler registration
- Background task initialization

The module serves as the central point for bot setup and configuration.
"""

import asyncio
from config import Config, bot
from telebot import asyncio_filters
from telebot.states.asyncio.middleware import StateMiddleware
from bot.middlewares import Middleware
from bot.handlers import setup_handlers
from bot.members_checker import start_members_checker
from bot.admin import setup_admin_functions

async def StartBot():
    """
    Initialize and start the Telegram bot.

    This function:
    1. Sets up state management filters
    2. Configures middleware for state and user management
    3. Registers message and callback handlers
    4. Initializes admin functionality
    5. Starts the background member checker
    6. Begins polling for updates

    The bot is configured to handle:
    - Chat member updates
    - Messages
    - Callback queries
    """
    # Add state filter for handling user states
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    
    # Setup middleware for state management and user processing
    bot.setup_middleware(StateMiddleware(bot))
    bot.setup_middleware(Middleware())

    # Register message handlers and admin functions
    setup_handlers(bot)
    setup_admin_functions(bot)
    
    # Start background task for checking member status
    asyncio.create_task(start_members_checker())

    # Start polling for updates
    await bot.polling(allowed_updates=["chat_member", "message", "callback_query"])
