"""
GroupManager Class

This class provides core functionality for managing Telegram group operations including:
- Creating invite links
- Managing member access
- Handling administrative actions

The class interfaces directly with the Telegram Bot API to perform group management tasks.
"""

from config import Config, bot

class GroupManager:
    """
    A class that handles all group-related operations for the Telegram bot.

    This class provides methods for managing group memberships, creating invite links,
    and handling administrative actions within the configured Telegram group.

    Attributes:
        chat_id (str): The Telegram chat ID of the managed group, loaded from config
    """

    def __init__(self):
        """Initialize GroupManager with the configured group chat ID."""
        self.chat_id = Config["GROUP_CHAT_ID"]

    async def CreateInviteLink(self, user_id: int | str) -> str:
        """
        Create a single-use invite link for a specific user.

        Args:
            user_id (int | str): The Telegram user ID for whom to create the invite link

        Returns:
            str: The generated invite link URL
        """
        InviteObj = await bot.create_chat_invite_link(
            chat_id = self.chat_id,
            name = f"{user_id}",
            member_limit = 1
        )
        return InviteObj.invite_link

    async def KickMember(self, user_id: int | str) -> None:
        """
        Remove a member from the group.

        This method bans and then immediately unbans the user to remove them
        from the group without preventing them from rejoining later.

        Args:
            user_id (int | str): The Telegram user ID of the member to remove
        """
        await bot.ban_chat_member(self.chat_id, user_id)
        await bot.unban_chat_member(self.chat_id, user_id)

    async def isMemberInGroup(self, user_id: int | str) -> bool:
        """
        Check if a user is currently a member of the group.

        Args:
            user_id (int | str): The Telegram user ID to check

        Returns:
            bool: True if the user is a member, False otherwise
        """
        inGroup = await bot.get_chat_member(self.chat_id, user_id)
        return True if inGroup and inGroup.status == 'member' else False
    
    async def GetAdmins(self):
        """
        Get a list of all administrators in the group.

        Returns:
            list: List of ChatMember objects representing group administrators
        """
        admins = await bot.get_chat_administrators(self.chat_id)
        return admins
