"""
Database Models Module

This module defines the SQLAlchemy ORM models for the bot's database schema.
It includes models for:
- Users and their attributes
- Subscription data
- System configurations

The models use SQLAlchemy's declarative base system for defining database tables
and their relationships.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, JSON
from datetime import datetime

from config import Config

Base = declarative_base()

class User(Base):
    """
    User Model

    Represents a Telegram user in the database with their associated data
    including chat information, personal details, and subscription status.

    Attributes:
        chat_id (BigInteger): Primary key, Telegram chat ID
        user_id (BigInteger): Telegram user ID
        fullname (String): User's full name
        email (String): User's email address
        username (String): Telegram username
        banned (Boolean): User ban status
        inGroup (Boolean): Whether user is in the group
        lang (String): User's preferred language
        subscription_data (JSON): Subscription details and status
    """
    __tablename__ = 'users'

    chat_id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    fullname = Column(String(50), unique=True)
    email = Column(String(200), unique=True)
    username = Column(String(50), unique=True, nullable=False)
    banned = Column(Boolean, default=False)
    inGroup = Column(Boolean, default=False)
    lang = Column(String(5), default=Config["DEFAULT_LANGUAGE"])
    subscription_data = Column(JSON)

    def to_dict(self):
        """
        Convert the user object to a dictionary.

        Returns:
            dict: Dictionary containing all user attributes
        """
        return {
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "fullname": self.fullname,
            "email": self.email,
            "username": self.username,
            "banned": self.banned,
            "lang": self.lang,
            "subscription_data": self.subscription_data,
        }
    
# Commented out Transaction model for future implementation
# class Transaction(Base):
#     __tablename__ = 'transactions'
#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     chat_id = Column(Integer, nullable=False)
#     currency = Column(String(3), nullable=False)
#     amount = Column(Float, nullable=False)
#     _type = Column(String(20), nullable=False)
#     description = Column(String(50))
#     time = Column(DateTime, default=datetime.now)
