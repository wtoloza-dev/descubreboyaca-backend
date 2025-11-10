"""Auth dependencies.

This module provides dependency injection factories for auth-related
operations including authentication, authorization, and user management.

All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from app.domains.auth.infrastructure.dependencies.auth import (
    get_current_user_dependency,
    get_optional_user_dependency,
    require_admin_dependency,
    require_owner_dependency,
)
from app.domains.auth.infrastructure.dependencies.security import (
    get_google_oauth_client_dependency,
    get_password_hasher_dependency,
    get_token_provider_dependency,
)
from app.domains.auth.infrastructure.dependencies.sql import (
    get_auth_service_dependency,
    get_user_repository_dependency,
)


__all__ = [
    # Auth
    "get_current_user_dependency",
    "get_optional_user_dependency",
    "require_admin_dependency",
    "require_owner_dependency",
    # Security services
    "get_password_hasher_dependency",
    "get_token_provider_dependency",
    "get_google_oauth_client_dependency",
    # SQL
    "get_auth_service_dependency",
    "get_user_repository_dependency",
]
