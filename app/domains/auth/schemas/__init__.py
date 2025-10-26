"""Auth domain schemas.

This module contains request/response schemas for auth API endpoints.
"""

from app.domains.auth.schemas.google_callback import (
    GoogleCallbackUserSchemaResponse,
)
from app.domains.auth.schemas.google_login import GoogleLoginUserSchemaResponse
from app.domains.auth.schemas.login import (
    LoginUserSchemaRequest,
    LoginUserSchemaResponse,
)
from app.domains.auth.schemas.me import MeUserSchemaResponse
from app.domains.auth.schemas.refresh import (
    RefreshUserSchemaRequest,
    RefreshUserSchemaResponse,
)
from app.domains.auth.schemas.register import (
    RegisterUserSchemaRequest,
    RegisterUserSchemaResponse,
)
from app.domains.auth.schemas.user import UserSchemaResponse


__all__ = [
    "RegisterUserSchemaRequest",
    "RegisterUserSchemaResponse",
    "LoginUserSchemaRequest",
    "LoginUserSchemaResponse",
    "RefreshUserSchemaRequest",
    "RefreshUserSchemaResponse",
    "UserSchemaResponse",
    "MeUserSchemaResponse",
    "GoogleLoginUserSchemaResponse",
    "GoogleCallbackUserSchemaResponse",
]
