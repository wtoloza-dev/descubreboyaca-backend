"""Favorite domain exceptions.

This module defines custom exceptions for the favorites domain.
"""

from app.shared.domain.exceptions import AlreadyExistsException, NotFoundException


class FavoriteAlreadyExistsError(AlreadyExistsException):
    """Raised when attempting to create a duplicate favorite.

    This exception is raised when a user tries to favorite an entity
    that they have already favorited.
    """

    def __init__(self, user_id: str, entity_type: str, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity
        """
        self.user_id = user_id
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(
            entity_type="Favorite",
            identifier=f"{user_id}:{entity_type}:{entity_id}",
        )


class FavoriteNotFoundError(NotFoundException):
    """Raised when a favorite is not found.

    This exception is raised when attempting to access or delete a favorite
    that doesn't exist.
    """

    def __init__(self, user_id: str, entity_type: str, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity
        """
        self.user_id = user_id
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(
            entity_type="Favorite",
            entity_id=f"{user_id}:{entity_type}:{entity_id}",
        )
