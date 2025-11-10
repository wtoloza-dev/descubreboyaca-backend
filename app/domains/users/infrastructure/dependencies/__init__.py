"""User dependencies package."""

from app.domains.users.infrastructure.dependencies.user import (
    get_user_service_dependency,
)


__all__ = ["get_user_service_dependency"]
