"""Base settings module."""

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base application settings."""

    # Environment settings
    SCOPE: str = "local"
    DEBUG: bool = True

    # Application settings
    APP_NAME: str = "Descubre Boyacá API"
    APP_VERSION: str = "0.0.1"
    APP_DESCRIPTION: str = "Backend API for Descubre Boyacá platform"
