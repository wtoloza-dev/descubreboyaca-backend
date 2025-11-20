"""Find users use case."""

from app.domains.users.domain import User
from app.domains.users.domain.interfaces import UserRepositoryInterface


class FindUsersUseCase:
    """Use case for finding users with pagination.

    Attributes:
        user_repository: Repository for user persistence
    """

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        """Initialize use case.

        Args:
            user_repository: User repository implementation
        """
        self.user_repository = user_repository

    async def execute(self, offset: int = 0, limit: int = 20) -> tuple[list[User], int]:
        """Execute the find users use case.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            tuple[list[User], int]: Tuple of (list of users, total count)
        """
        # Get users from repository
        users = await self.user_repository.find(
            filters=None, offset=offset, limit=limit
        )

        # Get total count
        total = await self.user_repository.count(filters=None)

        return users, total
