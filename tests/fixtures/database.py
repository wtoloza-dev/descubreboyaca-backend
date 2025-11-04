"""Database fixtures for testing.

This module provides database engine and session fixtures used across all tests.
Each test gets a fresh file-based SQLite database that is automatically cleaned up.
"""

import os
import tempfile

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture(name="test_engine", scope="function")
async def fixture_test_engine():
    """Create a test database engine with file-based SQLite.

    Each test gets a fresh file-based database that is automatically cleaned up.
    Using file DB instead of in-memory to avoid transaction isolation issues with TestClient.

    Returns:
        AsyncEngine: Async engine for testing
    """
    # Import all models to ensure they're registered with SQLModel
    from app.domains.audit.models import ArchiveModel  # noqa: F401
    from app.domains.auth.models import UserModel  # noqa: F401
    from app.domains.favorites.models import FavoriteModel  # noqa: F401
    from app.domains.restaurants.models import (  # noqa: F401
        DishModel,
        RestaurantModel,
        RestaurantOwnerModel,
    )

    # Create temporary file for test database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    # Create file-based database engine
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        echo=False,  # Set to True for SQL debugging
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()

    # Clean up temp file
    try:
        os.unlink(db_path)
    except Exception:
        pass


@pytest.fixture(name="test_session", scope="function")
async def fixture_test_session(test_engine):
    """Create a test database session.

    This fixture provides a clean async database session for each test.
    The session shares the same engine as test_client to ensure data visibility.

    Args:
        test_engine: Test database engine

    Returns:
        AsyncSession: Async session for testing

    Example:
        >>> async def test_create_restaurant(test_session):
        ...     restaurant = RestaurantModel(name="Test")
        ...     test_session.add(restaurant)
        ...     await test_session.commit()
    """
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session
