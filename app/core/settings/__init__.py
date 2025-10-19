"""Settings module.

This module provides environment-specific settings using a factory pattern
based on the SCOPE environment variable.
"""

import os
import re

from app.core.settings.base import BaseAppSettings
from app.core.settings.local import LocalSettings
from app.core.settings.prod import ProdSettings
from app.core.settings.staging import StagingSettings


def get_settings() -> BaseAppSettings:
    """Get settings based on SCOPE environment variable.

    Uses regex pattern matching to determine which settings class to instantiate.
    Patterns:
    - local: matches "local" exactly (case-insensitive)
    - staging**: matches anything starting with "staging" (staging, staging-test, etc.)
    - prod**: matches anything starting with "prod" (production, prod-us, etc.)

    Returns:
        BaseAppSettings: Settings instance for the current environment

    Raises:
        ValueError: If SCOPE doesn't match any known pattern
    """
    scope = os.getenv("SCOPE", "local")

    # Regex patterns for environment matching (case-insensitive)
    if re.match(r"^local$", scope, re.IGNORECASE):
        return LocalSettings()
    elif re.match(r"^staging", scope, re.IGNORECASE):
        return StagingSettings()
    elif re.match(r"^prod", scope, re.IGNORECASE):
        return ProdSettings()
    else:
        raise ValueError(
            f"Invalid SCOPE value: '{scope}'. "
            "Must be 'local', or start with 'staging' or 'prod'"
        )


# Global settings instance
settings = get_settings()


__all__ = ["settings", "get_settings", "BaseAppSettings"]
