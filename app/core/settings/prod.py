"""Production environment settings."""

from app.core.settings.base import BaseAppSettings


class ProdSettings(BaseAppSettings):
    """Production environment settings."""

    SCOPE: str = "prod"
