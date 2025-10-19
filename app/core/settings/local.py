"""Local development settings."""

from app.core.settings.base import BaseAppSettings


class LocalSettings(BaseAppSettings):
    """Local development settings."""

    SCOPE: str = "local"
