"""Security-related dependencies.

This module provides dependency injection factories for security-related
services (password hashing, JWT tokens, OAuth).

All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from app.core.settings import settings
from app.domains.auth.services import (
    BcryptPasswordHasher,
    GoogleOAuthClient,
    JWTTokenProvider,
)


def get_password_hasher_dependency() -> BcryptPasswordHasher:
    """Get password hasher instance.

    Returns:
        BcryptPasswordHasher instance for password hashing and verification
    """
    return BcryptPasswordHasher()


def get_token_provider_dependency() -> JWTTokenProvider:
    """Get token provider instance.

    Returns:
        JWTTokenProvider instance for JWT token operations
    """
    return JWTTokenProvider(
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
    )


def get_google_oauth_client_dependency() -> GoogleOAuthClient:
    """Get Google OAuth client instance.

    Returns:
        GoogleOAuthClient instance for Google OAuth operations
    """
    return GoogleOAuthClient(
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )
