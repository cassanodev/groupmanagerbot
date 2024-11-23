"""
User Utility Module

This module provides utility functions for user management including:
- User instance caching
- User creation and initialization
- Admin privilege verification
- User data management

The module serves as a central point for user-related operations
and maintains a cache of user instances for improved performance.
"""

from classes.User import User
from classes.GroupManager import GroupManager as GM
from database import MySQL
from config import Config

# Cache for storing user instances
users = {}

async def GetUser(user_id):
    """
    Get or create a User instance for the specified user ID.

    This function implements a caching mechanism to avoid recreating
    User instances unnecessarily. If the user exists in cache, it
    updates their data and returns the cached instance.

    Args:
        user_id: Telegram user ID

    Returns:
        User: Instance of User class for the specified ID
    """
    if user_id not in users:
        newUser = User(user_id)
        await newUser.init_asyncs()
        users[user_id] = newUser

    user = users[user_id]
    await user.load_data()
    return user

async def check_user(message):
    """
    Verify and initialize user data if needed.

    This function checks if a user exists in the database and creates
    a new user record if they don't. It's typically called when a user
    first interacts with the bot.

    Args:
        message: Telegram message object containing user information
    """
    user_id = message.from_user.id 
    user_data = await MySQL.GetUserById(user_id)

    if not user_data:
        await MySQL.CreateUser(
            chat_id=user_id,
            user_id=user_id,
            fullname=f"{message.from_user.first_name} {message.from_user.last_name}",
            username=message.from_user.username,
            lang=message.from_user.language_code or Config["DEFAULT_LANGUAGE"],
        )

async def is_admin(user_id: int | str) -> bool: 
    """
    Check if a user has admin privileges.

    This function verifies whether a user is an administrator in the
    configured Telegram group.

    Args:
        user_id (int | str): Telegram user ID to check

    Returns:
        bool: True if user is an admin, False otherwise
    """
    GroupManager = GM()
    admins = await GroupManager.GetAdmins()
    isAdmin = next((True for admin in admins if user_id == admin.user.id), False)
    return isAdmin
