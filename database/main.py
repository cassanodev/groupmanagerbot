"""
Database Initialization Module

This module handles the initialization and setup of the database including:
- Engine creation
- Table creation
- Schema management

The module uses SQLAlchemy's async engine for database operations and ensures
all necessary tables are created at application startup.
"""

from sqlalchemy.ext.asyncio import create_async_engine
from database.models import Base 
from config import Config

# Create async engine using connection string from config
database_url = Config["DB_CONNECTION_STRING"]
engine = create_async_engine(database_url, future=True)

async def create_tables():
    """
    Create all database tables defined in the models.

    This function is called during application startup to ensure all
    necessary database tables exist. It uses SQLAlchemy's create_all
    method to create any missing tables based on the defined models.

    The function:
    1. Connects to the database
    2. Creates tables if they don't exist
    3. Maintains existing tables if they do exist

    Note:
        This function is safe to call multiple times as it only creates
        tables that don't already exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
