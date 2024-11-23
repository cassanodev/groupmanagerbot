"""
MySQL Database Operations Module

This module provides database operations for the bot using SQLAlchemy with async support.
It handles all database interactions including:
- User creation and retrieval
- Data updates
- Bulk operations

The module uses SQLAlchemy's async engine and session management for all database operations.
"""

import sys
import os
from typing import Any
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from models import User

database_url = Config["DB_CONNECTION_STRING"]
engine = create_async_engine(database_url, future=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def CreateUser(chat_id: int | str, user_id: int | str, fullname: str, username: str, lang: str):
    """
    Create a new user in the database.

    Args:
        chat_id (int | str): Telegram chat ID
        user_id (int | str): Telegram user ID
        fullname (str): User's full name
        username (str): User's Telegram username
        lang (str): User's preferred language code

    Returns:
        User: The newly created user object
    """
    async with async_session() as session:
        new_user = User(
            chat_id=chat_id,
            user_id=user_id,
            fullname=fullname,
            username=username,
            lang=lang,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  

    return new_user

async def GetUserById(user_id: int):
    """
    Retrieve a user by their Telegram user ID.

    Args:
        user_id (int): Telegram user ID to search for

    Returns:
        User: User object if found, None otherwise
    """
    async with async_session() as session:
        result = await session.execute(select(User).filter(User.user_id == user_id))
        user = result.scalars().first()
    
    return user

async def GetUserByField(field: str, value: Any):
    """
    Retrieve a user by any field value.

    Args:
        field (str): The field name to search by
        value (Any): The value to search for

    Returns:
        User: User object if found, None if field doesn't exist or user not found
    """
    field_attr = getattr(User, field, None)

    if field_attr is None:
        return None
    
    async with async_session() as session:
        result = await session.execute(select(User).filter(field_attr == value))
        user = result.scalars().first()
    
    return user

async def UpdateFieldForUser(user_id: int, field: str, value: Any):
    """
    Update a specific field for a user.

    Args:
        user_id (int): Telegram user ID of the user to update
        field (str): Name of the field to update
        value (Any): New value for the field

    Returns:
        bool: True if update was successful, False if field doesn't exist
    """
    field_attr = getattr(User, field, None)
    if field_attr is None:
        return False 
    
    async with async_session() as session:
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values({field_attr: value})
        )
        await session.execute(stmt)
        await session.commit()

    return True

async def GetAllUsers():
    """
    Retrieve all users from the database.

    Returns:
        list: List of all User objects in the database.
        If an error occurs, returns an empty list.
    """
    async with async_session() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users
        except Exception as e:
            print(f"Error while getting users: {e}")
            return []
