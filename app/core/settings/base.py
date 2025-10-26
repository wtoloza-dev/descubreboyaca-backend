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

    # JWT Authentication settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production-min-32-characters"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth2 settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"

    # CORS settings
    CORS_ORIGINS: str = "*"  # Allow all origins
