"""Alembic environment configuration for Descubre Boyacá Backend.

This module configures Alembic to work with SQLModel and supports both
online (connected to DB) and offline (SQL generation) modes.
"""

from logging.config import fileConfig

# Import all models to ensure they're registered with SQLModel metadata
from app.domains.audit.models.archive import ArchiveModel  # noqa: F401
from app.domains.auth.models.user import UserModel  # noqa: F401
from app.domains.favorites.models.favorite import FavoriteModel  # noqa: F401
from app.domains.restaurants.models.dish import DishModel  # noqa: F401
from app.domains.restaurants.models.restaurant import RestaurantModel  # noqa: F401
from app.domains.restaurants.models.restaurant_owner import (  # noqa: F401
    RestaurantOwnerModel,
)
from app.domains.reviews.models.review import ReviewModel  # noqa: F401
from sqlalchemy import engine_from_config, pool

# Import SQLModel metadata
from sqlmodel import SQLModel

from alembic import context

# Import settings to get database URL
from app.core.settings import settings


# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = SQLModel.metadata


# Override sqlalchemy.url with app settings
# This allows using environment variables for different environments
def get_url() -> str:
    """Get database URL based on environment."""
    if settings.SCOPE == "local":
        return "sqlite:///./local.db"
    elif settings.SCOPE == "staging":
        # TODO: Add staging database URL from settings
        return "postgresql://user:pass@staging-db:5432/descubreboyaca"
    elif settings.SCOPE == "prod":
        # TODO: Add production database URL from settings
        return "postgresql://user:pass@prod-db:5432/descubreboyaca"
    else:
        raise ValueError(f"Unknown SCOPE: {settings.SCOPE}")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an
    Engine is acceptable here as well. By skipping the Engine creation we
    don't even need a DBAPI to be available.

    Calls to context.exec() here emit the given string to the script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    # Override the sqlalchemy.url in the alembic config
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
