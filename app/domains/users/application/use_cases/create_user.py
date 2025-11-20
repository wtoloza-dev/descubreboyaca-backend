"""Create user use case."""

from app.domains.auth.domain.interfaces import PasswordHasher
from app.domains.users.domain import User, UserData
from app.domains.users.domain.enums import AuthProvider
from app.domains.users.domain.exceptions import UserAlreadyExistsException
from app.domains.users.domain.interfaces import UserRepositoryInterface
from app.domains.users.domain.value_objects import CreateUserData


class CreateUserUseCase:
    """Use case for creating a new user.

    This use case follows DDD patterns by:
    1. Receiving a domain value object (CreateUserData) with user creation data
    2. Validating business rules (email uniqueness)
    3. Applying domain logic (password hashing)
    4. Building the User entity with proper value objects (UserData)
    5. Persisting through repository

    Attributes:
        user_repository: Repository for user persistence
        password_hasher: Hasher for password operations
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_hasher: PasswordHasher,
    ) -> None:
        """Initialize use case.

        Args:
            user_repository: User repository implementation
            password_hasher: Password hasher implementation
        """
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def execute(self, user_data: CreateUserData, created_by: str) -> User:
        """Execute the create user use case.

        Args:
            user_data: Value object containing user creation data (before hashing)
            created_by: Admin user ID who is creating this user

        Returns:
            User: Created user entity

        Raises:
            UserAlreadyExistsException: If email is already registered
        """
        # Validate business rule: email uniqueness
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(str(user_data.email))

        # Apply domain logic: hash password
        hashed_password = self.password_hasher.hash_password(user_data.password)

        # Build UserData value object with hashed password
        user_entity_data = UserData(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password.value,
            role=user_data.role,
            is_active=user_data.is_active,
            auth_provider=AuthProvider.EMAIL,
        )

        # Create and persist user entity
        user = await self.user_repository.create(
            user_entity_data, created_by=created_by
        )

        return user
