"""Favorites dependency injection factories."""

from app.domains.favorites.infrastructure.dependencies.favorite import (
    get_favorite_repository_dependency,
    get_favorite_service_dependency,
)


__all__ = [
    "get_favorite_repository_dependency",
    "get_favorite_service_dependency",
]
