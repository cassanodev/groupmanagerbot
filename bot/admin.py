"""
Admin Module

This module implements administrative functionality for the bot including:
- Subscription management
- User privilege handling
- Administrative commands
- Subscription time management

The module provides secure admin-only commands for managing user subscriptions
and group access.
"""

from telebot import types
from telebot.states.asyncio.context import StateContext
from typing import Dict, Any, Union
from database import MySQL
from utils.user import GetUser, is_admin
from classes.User import User as UserClass
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.util import quick_markup
from datetime import datetime, timedelta

class AdminStates(StatesGroup):
    """
    State definitions for admin operations.

    This class defines the various states used in admin operations:
    - AskId: State for requesting user ID
    - AskTime: State for requesting subscription duration
    """
    AskId = State()
    AskTime = State()

def setup_admin_functions(bot):
    """
    Set up administrative command handlers for the bot.

    Args:
        bot: The bot instance to attach handlers to
    """

    @bot.message_handler(commands='add_sub', chat_types=['private'])
    async def add_sub(message: types.Message, state: StateContext):
        """
        Handle the add_sub command for adding user subscriptions.

        This command allows administrators to add or extend user subscriptions.
        It initiates a multi-step process for specifying the user and duration.

        Args:
            message: The command message
            state: State context for managing conversation state
        """
        user_id = message.chat.id
        if not await is_admin(user_id):
            return
        
        User: UserClass = await GetUser(user_id)
        text: str = User.locales['admin:ask_id']
        
        await state.set(AdminStates.AskId)
        await User.SendMessage(text)

    @bot.message_handler(state=AdminStates.AskId)
    async def ask_time(message: types.Message, state: StateContext):
        """
        Handle the user ID input state.

        Validates the provided user ID and prompts for subscription duration.

        Args:
            message: Message containing user ID
            state: State context for managing conversation state
        """
        user_id = message.chat.id
        if not await is_admin(user_id):
            return
        
        User = await GetUser(user_id)
        
        target_user_id = message.text.strip()
        target_user_exists = await MySQL.GetUserById(target_user_id)

        if not target_user_exists:
            await User.SendMessage(User.locales["userNotFound"])
            return 
        
        await state.add_data(target_user_id=target_user_id)
        await state.set(AdminStates.AskTime)
        await User.SendMessage(User.locales["admin:ask_time"])

    @bot.message_handler(state=AdminStates.AskTime)
    async def confirm_details(message: types.Message, state: StateContext):
        """
        Handle the subscription duration input state.

        Validates the duration and updates the user's subscription accordingly.

        Args:
            message: Message containing subscription duration
            state: State context for managing conversation state
        """
        user_id = message.chat.id
        if not await is_admin(user_id):
            return
        
        User = await GetUser(user_id)
        exp_time = message.text.strip()
        if not exp_time.isdigit():
            await User.SendMessage(User.locales["admin:invalid_time"])
            return

        async with state.data() as data:
            target_user_id = data.get("target_user_id")
            now = datetime.now()
            expiration_date = now + timedelta(hours=int(exp_time))
            await MySQL.UpdateFieldForUser(target_user_id, "subscription_data", {
                "expiration_date": expiration_date.timestamp()
            })

            await state.delete()
            await User.SendMessage(User.locales["admin:success"].format(id=target_user_id))
