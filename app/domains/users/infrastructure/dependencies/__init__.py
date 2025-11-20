"""User dependencies package."""

# Repository dependencies
from app.domains.users.infrastructure.dependencies.repository import (
    get_user_repository_dependency,
)

# Use case dependencies
from app.domains.users.infrastructure.dependencies.use_cases import (
    get_create_user_use_case_dependency,
    get_delete_user_use_case_dependency,
    get_find_users_use_case_dependency,
)

# Legacy service dependency (DEPRECATED - use use cases instead)
from app.domains.users.infrastructure.dependencies.user import (
    get_user_service_dependency,
)


__all__ = [
    # Repository
    "get_user_repository_dependency",
    # Use cases
    "get_create_user_use_case_dependency",
    "get_delete_user_use_case_dependency",
    "get_find_users_use_case_dependency",
    # Legacy (DEPRECATED)
    "get_user_service_dependency",
]
