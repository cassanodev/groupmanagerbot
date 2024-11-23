"""
User Class

This module provides the User class which handles all user-specific operations including:
- Message sending and editing
- User data management
- Localization support
- Photo message handling
"""

import os 
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config, bot
from database import MySQL

class User:
    """
    A class that handles user-specific operations and data management.

    This class provides methods for interacting with individual users, managing their data,
    and handling message operations specific to each user.

    Attributes:
        user_id (int): The Telegram user ID
        user_data (object): User data from the database
        locales (dict): Loaded localization strings
        last_message_id (int): ID of the last sent message
    """

    def __init__(self, user_id):
        """
        Initialize a User instance.

        Args:
            user_id (int): The Telegram user ID
        """
        self.user_id = user_id
        self.user_data = None
        self.locales = None
        self.last_message_id = None
            
    async def SendMessage(self, text: str, parse_mode: str = "Html", reply_markup: list = None, protect_content = False):
        """
        Send a message to the user.

        Args:
            text (str): The message text to send
            parse_mode (str, optional): Message parsing mode. Defaults to "Html"
            reply_markup (list, optional): Keyboard markup. Defaults to None
            protect_content (bool, optional): Whether to protect content. Defaults to False

        Returns:
            Message: The sent message object
        """
        result = await bot.send_message(
            chat_id=self.user_data.chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            protect_content=protect_content
        )
        self.last_message_id = result.message_id
        return result
    
    async def SendPhoto(self, image_url: str, text: str, parse_mode: str = "Html", reply_markup: list = None):
        """
        Send a photo with caption to the user.

        Args:
            image_url (str): URL of the image to send
            text (str): Caption text for the image
            parse_mode (str, optional): Message parsing mode. Defaults to "Html"
            reply_markup (list, optional): Keyboard markup. Defaults to None

        Returns:
            Message: The sent message object
        """
        result = await bot.send_photo(
            chat_id=self.user_data.chat_id,
            photo=image_url,
            caption=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        self.last_message_id = None
        return result

    async def EditMessage(self, text: str, parse_mode: str = "Html", reply_markup: list = None):
        """
        Edit the last sent message.

        If editing fails, sends a new message instead.

        Args:
            text (str): New text for the message
            parse_mode (str, optional): Message parsing mode. Defaults to "Html"
            reply_markup (list, optional): Keyboard markup. Defaults to None
        """
        try:
            await bot.edit_message_text(
                chat_id=self.user_data.chat_id,
                message_id=self.last_message_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        except:
            await self.SendMessage(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )

    async def init_asyncs(self):
        """
        Initialize async components by loading user data and localization strings.
        
        This method must be called after creating a new User instance to load
        the necessary data from the database and localization files.
        """
        await self.load_data()
        await self.load_locales()

    async def load_data(self):
        """
        Load user data from the database.
        
        Retrieves the user's data from the database and stores it in the user_data attribute.
        This includes information like chat_id, language preferences, and subscription status.
        """
        user = await MySQL.GetUserById(user_id=self.user_id)
        self.user_data = user

    async def load_locales(self):
        """
        Load localization strings for the user's preferred language.
        
        Loads the appropriate language file based on the user's language preference.
        Falls back to the default language if the preferred language file is not found.
        """
        default_language = Config["DEFAULT_LANGUAGE"]
        lang_file = f"locales/{self.user_data.lang}.json"
        
        if not os.path.isfile(lang_file):
            lang_file = f"locales/{default_language}.json"
        
        with open(lang_file, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
        
        self.locales = lang_data
