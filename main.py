"""
GroupManagerBot - Main Entry Point

This module serves as the main entry point for the GroupManagerBot application. It initializes
the bot, sets up the database tables, and starts the bot's polling mechanism.

The bot is designed to manage Telegram group memberships with features including:
- Subscription management
- Payment processing
- Group access control
- Administrative functions

Dependencies:
    - asyncio: For asynchronous operation
    - config: Bot configuration and settings
    - database.main: Database initialization
    - utils.logger: Logging configuration
    - bot.instance: Bot instance and setup
"""

import asyncio
from config import Config
from database.main import create_tables
from utils.logger import get_logger
from bot.instance import StartBot

logger = get_logger(__name__)

async def main() -> None:
    """
    Main asynchronous function that initializes and starts the bot.
    
    This function:
    1. Creates necessary database tables
    2. Initializes the bot instance
    3. Starts the bot's polling mechanism
    4. Handles any critical errors during operation
    
    Raises:
        Exception: If any critical error occurs during bot initialization or operation
    """
    try:
        await create_tables()
        logger.info("Bot running.")
        await StartBot()
    except Exception as e:
        logger.error("Critical error in the bot: %s", e, exc_info=True)
        raise

if __name__ == '__main__':
    asyncio.run(main())
