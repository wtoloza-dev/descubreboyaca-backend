"""Fixtures for auth domain tests.

This module provides domain-specific fixtures for authentication tests,
including user creation, password handling, token generation, and auth service setup.
"""

from dataclasses import dataclass

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain import User, UserData
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.models import UserModel
from app.domains.auth.repositories.user import UserRepositorySQLite
from app.domains.auth.services import AuthService, BcryptPasswordHasher
from app.domains.auth.services.token import JWTTokenProvider
from app.shared.domain.factories import generate_ulid


@dataclass
class TestPassword:
    """Test password credentials with plain and hashed versions.

    Attributes:
        password: Plain text password
        hashed_password: Bcrypt hashed version of the password
    """

    password: str
    hashed_password: str


@pytest.fixture(name="test_password")
def fixture_test_password() -> TestPassword:
    """Provide test password credentials.

    Returns:
        TestPassword: Object containing plain password and its bcrypt hash

    Example:
        >>> def test_login(test_password):
        ...     user = create_user(hashed_password=test_password.hashed_password)
        ...     login(email=user.email, password=test_password.password)
    """
    return TestPassword(
        password="password123",
        hashed_password="$2b$12$BDL2XhQDe5ylzT/iEDySpeq4DlqfN1XS3Dd3XjAePo8eHbnQ1gbbC",
    )


@pytest.fixture(name="create_test_user")
def fixture_create_test_user(test_session: AsyncSession, test_password: TestPassword):
    """Factory fixture for creating test users.

    This fixture provides a callable that creates users with customizable
    attributes. Defaults are provided for all required fields.

    Args:
        test_session: Database session for persistence
        test_password: Test password credentials

    Returns:
        Async callable that creates and persists a user

    Example:
        >>> user = await create_test_user(email="test@example.com")
        >>> user = await create_test_user(
        ...     email="admin@example.com", role=UserRole.ADMIN
        ... )
    """

    async def _create(**kwargs) -> User:
        """Create a test user with custom attributes.

        Args:
            **kwargs: User attributes to override defaults

        Returns:
            User: Created and persisted user entity
        """
        # Create user data with defaults
        user_data = UserData(
            email=kwargs.get("email", f"user_{generate_ulid()}@test.com"),
            full_name=kwargs.get("full_name", "Test User"),
            hashed_password=kwargs.get(
                "hashed_password",
                test_password.hashed_password,
            ),
            role=kwargs.get("role", UserRole.USER),
            is_active=kwargs.get("is_active", True),
            auth_provider=kwargs.get("auth_provider", AuthProvider.EMAIL),
            google_id=kwargs.get("google_id"),
            profile_picture_url=kwargs.get("profile_picture_url"),
        )

        # Create user entity
        user = User(id=kwargs.get("id", generate_ulid()), **user_data.model_dump())

        # Convert to ORM model and persist
        model = UserModel.model_validate(user)
        test_session.add(model)
        await test_session.commit()
        await test_session.refresh(model)

        # Return as entity
        return User.model_validate(model)

    return _create


@pytest.fixture(name="password_service")
def fixture_password_service() -> BcryptPasswordHasher:
    """Create a password service instance for testing.

    Returns:
        BcryptPasswordHasher: Configured password hasher

    Example:
        >>> def test_password_hashing(password_service):
        ...     hashed = password_service.hash_password("mypassword")
        ...     assert password_service.verify_password("mypassword", hashed)
    """
    return BcryptPasswordHasher()


@pytest.fixture(name="token_provider")
def fixture_token_provider() -> JWTTokenProvider:
    """Create a JWT token provider instance for testing.

    Uses test-safe configuration with short expiration times.

    Returns:
        JWTTokenProvider: Configured token provider

    Example:
        >>> def test_token_generation(token_provider):
        ...     token = token_provider.create_access_token(user_id="123")
        ...     assert token_provider.decode_token(token)["sub"] == "123"
    """
    return JWTTokenProvider(
        secret_key="test-secret-key-for-testing-only",
        algorithm="HS256",
        access_token_expire_minutes=30,
        refresh_token_expire_days=7,
    )


@pytest.fixture(name="auth_service")
def fixture_auth_service(
    test_session: AsyncSession,
    token_provider: JWTTokenProvider,
    password_service: BcryptPasswordHasher,
) -> AuthService:
    """Create an auth service instance for testing.

    This fixture provides a fully configured AuthService with
    all required dependencies injected.

    Args:
        test_session: Database session
        token_provider: JWT token provider
        password_service: Password hashing service

    Returns:
        AuthService: Configured auth service

    Example:
        >>> async def test_registration(auth_service):
        ...     user = await auth_service.register(
        ...         email="test@example.com", password="password123"
        ...     )
        ...     assert user.email == "test@example.com"
    """
    user_repository = UserRepositorySQLite(test_session)
    return AuthService(
        user_repository=user_repository,
        token_provider=token_provider,
        password_hasher=password_service,
    )


@pytest.fixture(name="user_repository")
def fixture_user_repository(test_session: AsyncSession) -> UserRepositorySQLite:
    """Create a user repository instance for testing.

    Args:
        test_session: Database session

    Returns:
        UserRepositorySQLite: Configured user repository

    Example:
        >>> async def test_user_lookup(user_repository):
        ...     user = await user_repository.get_by_email("test@example.com")
    """
    return UserRepositorySQLite(test_session)
