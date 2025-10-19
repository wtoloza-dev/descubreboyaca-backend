"""Staging environment settings."""

from app.core.settings.base import BaseAppSettings


class StagingSettings(BaseAppSettings):
    """Staging environment settings."""

    SCOPE: str = "staging"
