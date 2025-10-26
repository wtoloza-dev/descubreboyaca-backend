"""Auth service implementation.

This module provides the main authentication service that orchestrates
user registration, login, and token management.
"""

from app.domains.auth.domain import (
    OAuthProfile,
    PasswordHash,
    TokenData,
    User,
    UserData,
)
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.domain.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.auth.domain.interfaces import (
    PasswordHasher,
    TokenProvider,
    UserRepositoryInterface,
)


class AuthService:
    """Main authentication service.

    This service orchestrates authentication operations including
    user registration, login, token refresh, and user retrieval.
    It supports both email/password and OAuth2 authentication.

    Attributes:
        user_repository: Repository for user persistence
        token_provider: Provider for JWT token operations
        password_hasher: Hasher for password hashing/verification
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        token_provider: TokenProvider,
        password_hasher: PasswordHasher,
    ) -> None:
        """Initialize auth service.

        Args:
            user_repository: User repository implementation
            token_provider: Token provider implementation
            password_hasher: Password hasher implementation
        """
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.password_hasher = password_hasher

    async def register(
        self, email: str, password: str, full_name: str, role: UserRole = UserRole.USER
    ) -> User:
        """Register a new user with email and password.

        Args:
            email: User's email address
            password: Plain text password
            full_name: User's full name
            role: User's role (default: USER)

        Returns:
            Created User entity

        Raises:
            UserAlreadyExistsException: If email is already registered
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)

        # Hash password
        hashed_password = self.password_hasher.hash_password(password)

        # Create user data
        user_data = UserData(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password.value,
            role=role,
            is_active=True,
            auth_provider=AuthProvider.EMAIL,
        )

        # Persist user
        user = await self.user_repository.create(user_data)

        return user

    async def login(self, email: str, password: str) -> tuple[TokenData, User]:
        """Authenticate user with email and password.

        Args:
            email: User's email address
            password: Plain text password

        Returns:
            Tuple of (TokenData with JWT tokens, User entity)

        Raises:
            InvalidCredentialsException: If credentials are invalid
            UserInactiveException: If user account is inactive
        """
        # Verify credentials and get user
        user = await self.verify_user_credentials(email, password)

        # Generate tokens
        tokens = self._generate_tokens(user)

        return tokens, user

    async def login_with_oauth(
        self, oauth_profile: OAuthProfile
    ) -> tuple[TokenData, User]:
        """Authenticate or register user using OAuth2 profile.

        If user doesn't exist, creates a new account.
        If user exists, logs them in.

        Args:
            oauth_profile: OAuth profile from provider (Google, etc.)

        Returns:
            Tuple of (TokenData with JWT tokens, User entity)

        Raises:
            UserInactiveException: If user account is inactive
        """
        # Try to find user by provider ID
        user = None
        if oauth_profile.provider == AuthProvider.GOOGLE:
            user = await self.user_repository.get_by_google_id(
                oauth_profile.provider_user_id
            )

        # If not found by provider ID, try email
        if not user:
            user = await self.user_repository.get_by_email(oauth_profile.email)

            # If found by email but different provider, update provider info
            if user and user.auth_provider != oauth_profile.provider:
                # Update user with OAuth provider info
                user_data = UserData(
                    email=user.email,
                    full_name=oauth_profile.full_name or user.full_name,
                    hashed_password=user.hashed_password,
                    role=user.role,
                    is_active=user.is_active,
                    auth_provider=oauth_profile.provider,
                    google_id=oauth_profile.provider_user_id
                    if oauth_profile.provider == AuthProvider.GOOGLE
                    else user.google_id,
                    profile_picture_url=oauth_profile.profile_picture_url
                    or user.profile_picture_url,
                )
                user = await self.user_repository.update(user.id, user_data)

        # If user still doesn't exist, create new account
        if not user:
            user_data = UserData(
                email=oauth_profile.email,
                full_name=oauth_profile.full_name,
                hashed_password=None,  # No password for OAuth users
                role=UserRole.USER,
                is_active=True,
                auth_provider=oauth_profile.provider,
                google_id=oauth_profile.provider_user_id
                if oauth_profile.provider == AuthProvider.GOOGLE
                else None,
                profile_picture_url=oauth_profile.profile_picture_url,
            )
            user = await self.user_repository.create(user_data)

        # Check if user is active
        if not user.is_active:
            raise UserInactiveException(user.email)

        # Generate tokens
        tokens = self._generate_tokens(user)

        return tokens, user

    async def refresh_access_token(self, refresh_token: str) -> TokenData:
        """Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New TokenData with fresh access token

        Raises:
            InvalidTokenException: If refresh token is invalid
            ExpiredTokenException: If refresh token has expired
            UserNotFoundException: If user no longer exists
        """
        # Verify refresh token
        payload = self.token_provider.verify_token(refresh_token)

        # Ensure it's a refresh token
        if payload.get("type") != "refresh":
            from app.domains.auth.domain.exceptions import InvalidTokenException

            raise InvalidTokenException("Invalid token type")

        # Get user ID from token
        user_id = payload.get("sub")
        if not user_id:
            from app.domains.auth.domain.exceptions import InvalidTokenException

            raise InvalidTokenException("Invalid token payload")

        # Get user from database
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        # Check if user is active
        if not user.is_active:
            raise UserInactiveException(user.email)

        # Generate new tokens
        return self._generate_tokens(user)

    async def get_current_user(self, token: str) -> User:
        """Get current user from access token.

        Args:
            token: Valid access token

        Returns:
            User entity

        Raises:
            InvalidTokenException: If token is invalid
            ExpiredTokenException: If token has expired
            UserNotFoundException: If user no longer exists
        """
        # Verify token
        payload = self.token_provider.verify_token(token)

        # Get user ID from token
        user_id = payload.get("sub")
        if not user_id:
            from app.domains.auth.domain.exceptions import InvalidTokenException

            raise InvalidTokenException("Invalid token payload")

        # Get user from database
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        # Check if user is active
        if not user.is_active:
            raise UserInactiveException(user.email)

        return user

    async def verify_user_credentials(self, email: str, password: str) -> User:
        """Verify user credentials.

        Args:
            email: User's email address
            password: Plain text password

        Returns:
            User entity if credentials are valid

        Raises:
            InvalidCredentialsException: If credentials are invalid
            UserInactiveException: If user account is inactive
        """
        # Get user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsException()

        # Check if user has a password (OAuth users don't have passwords)
        if not user.hashed_password:
            raise InvalidCredentialsException("This account uses OAuth authentication")

        # Verify password
        password_hash = PasswordHash(value=user.hashed_password)
        if not self.password_hasher.verify_password(password, password_hash):
            raise InvalidCredentialsException()

        # Check if user is active
        if not user.is_active:
            raise UserInactiveException(user.email)

        return user

    def _generate_tokens(self, user: User) -> TokenData:
        """Generate access and refresh tokens for a user.

        Args:
            user: User entity

        Returns:
            TokenData with access and refresh tokens
        """
        access_token = self.token_provider.create_access_token(
            user_id=user.id, email=user.email, role=user.role
        )
        refresh_token = self.token_provider.create_refresh_token(user_id=user.id)

        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
