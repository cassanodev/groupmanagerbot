"""
Members Checker Module

This module implements periodic membership verification functionality including:
- Subscription expiration checks
- Group membership validation
- Automatic member removal
- Admin privilege verification

The module runs continuous checks to ensure only valid subscribers and admins
remain in the group.
"""

import asyncio
from datetime import datetime, timezone
from utils.logger import get_logger

from database import MySQL
from classes.GroupManager import GroupManager as GM

logger = get_logger(__name__)

async def process_user(user, admins, GroupManager):
    """
    Process a single user's membership status.

    This function checks the user's subscription status and group membership,
    taking appropriate action if needed (e.g., removing expired members).

    Args:
        user: User object to process
        admins: List of group administrators
        GroupManager: Instance of GroupManager class
    """
    user_id = user.user_id
    User = await MySQL.GetUserById(user_id)
    subscription_data = User.subscription_data

    # Check subscription status
    if subscription_data:
        exp_date = datetime.fromtimestamp(int(subscription_data['expiration_date']), tz=timezone.utc)
        subscriptionActive = exp_date > datetime.now(timezone.utc)
    else:
        subscriptionActive = False

    # Handle expired or missing subscriptions
    if not subscriptionActive:
        isAdmin = next((True for admin in admins if user_id == admin.user.id), False)
        userInGroup = await GroupManager.isMemberInGroup(user_id)

        # Clear expired subscription data
        if subscription_data:
            await MySQL.UpdateFieldForUser(user.chat_id, "subscription_data", None)

        # Remove non-admin users with expired subscriptions
        if userInGroup and not isAdmin:
            await GroupManager.KickMember(user_id)

async def check_user_membership():
    """
    Check membership status for all users.

    This function:
    1. Retrieves all users from the database
    2. Gets current group administrators
    3. Processes each user's membership status concurrently
    """
    GroupManager = GM()
    users = await MySQL.GetAllUsers()
    admins = await GroupManager.GetAdmins()

    async with asyncio.TaskGroup() as tg:
        for user in users:
            tg.create_task(process_user(user, admins, GroupManager))

async def start_members_checker():
    """
    Start the continuous membership checking process.

    This function runs indefinitely, performing membership checks every 3 seconds.
    It ensures that only users with valid subscriptions or admin privileges
    remain in the group.
    """
    while True:
        await check_user_membership()
        await asyncio.sleep(3)  # Wait 3 seconds between checks
