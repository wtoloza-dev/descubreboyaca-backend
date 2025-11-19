# Settings Management

## Purpose

The settings system provides **environment-based configuration** using Pydantic Settings, allowing the application to adapt to different deployment environments (local, staging, production) without code changes.

## Key Concept

**12-Factor App Principle**: Store configuration in the environment, not in code.

```
Environment Variables (.env file)
    │
    │ loaded by
    ▼
Pydantic Settings (Validation)
    │
    │ provides
    ▼
Application Configuration
    │
    │ used by
    ▼
All Layers (Domains, Clients, Core)
```

## Settings Structure

### Base Settings Class

```python
# app/core/settings/base.py

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base application settings.

    Configuration is loaded from environment variables and .env file.
    Pydantic validates all values and provides type safety.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra env vars
    )

    # Environment
    SCOPE: str = Field(default="local", description="Environment: local, staging, prod")

    # Database
    DATABASE_URL: str = Field(..., description="Database connection URL")
    DATABASE_ECHO: bool = Field(default=False, description="Log SQL queries")

    # Security - JWT
    JWT_SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRATION_MINUTES: int = Field(default=30, description="JWT token expiration")

    # Security - OAuth2
    GOOGLE_CLIENT_ID: str | None = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: str | None = Field(default=None, description="Google OAuth secret")

    # CORS
    CORS_ORIGINS: list[str] = Field(default_factory=list, description="Allowed CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Allow credentials in CORS")

    # API
    API_V1_PREFIX: str = Field(default="/api/v1", description="API version 1 prefix")
    PROJECT_NAME: str = Field(default="Descubre Boyacá API", description="Project name")
    DEBUG: bool = Field(default=False, description="Debug mode")
```

### Environment-Specific Settings

#### Local Development

```python
# app/core/settings/local.py

from app.core.settings.base import Settings


class LocalSettings(Settings):
    """Development environment settings."""

    SCOPE: str = "local"
    DATABASE_URL: str = "sqlite+aiosqlite:///./local.db"
    DATABASE_ECHO: bool = True  # Log SQL in development
    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
```

#### Staging

```python
# app/core/settings/staging.py

from app.core.settings.base import Settings


class StagingSettings(Settings):
    """Staging environment settings."""

    SCOPE: str = "staging"
    # DATABASE_URL: Must be provided via environment variable
    DATABASE_ECHO: bool = True  # Still log SQL for debugging
    DEBUG: bool = False
    # CORS_ORIGINS: Must be provided via environment variable
```

#### Production

```python
# app/core/settings/prod.py

from app.core.settings.base import Settings


class ProdSettings(Settings):
    """Production environment settings."""

    SCOPE: str = "prod"
    # DATABASE_URL: Must be provided via environment variable
    DATABASE_ECHO: bool = False  # Don't log SQL in production
    DEBUG: bool = False
    # All sensitive values must come from secure environment variables
```

## Configuration Loading

### Factory Pattern

```python
# app/core/settings/__init__.py

from app.core.settings.base import Settings
from app.core.settings.local import LocalSettings
from app.core.settings.staging import StagingSettings
from app.core.settings.prod import ProdSettings


def get_settings() -> Settings:
    """Factory to create settings based on SCOPE environment variable.

    Returns:
        Settings: Environment-specific settings instance

    Example:
        >>> import os
        >>> os.environ["SCOPE"] = "prod"
        >>> settings = get_settings()
        >>> isinstance(settings, ProdSettings)
        True
    """
    import os

    scope = os.getenv("SCOPE", "local").lower()

    settings_map = {
        "local": LocalSettings,
        "staging": StagingSettings,
        "prod": ProdSettings,
    }

    settings_class = settings_map.get(scope, LocalSettings)
    return settings_class()


# Singleton instance
settings = get_settings()
```

### Usage Throughout Application

```python
# Any module can import and use settings
from app.core.settings import settings

# Access configuration
database_url = settings.DATABASE_URL
is_debug = settings.DEBUG
jwt_secret = settings.JWT_SECRET_KEY

# Environment detection
if settings.SCOPE == "prod":
    # Production-specific logic
    enable_monitoring()
```

## Environment Variables

### Required Variables

Must be set in all environments:

```bash
# .env

# Security
JWT_SECRET_KEY=your-super-secret-key-minimum-32-characters

# Database (format depends on environment)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

### Optional Variables

Have defaults but can be overridden:

```bash
# Environment
SCOPE=local  # Default: local

# Database
DATABASE_ECHO=true  # Default: false

# JWT
JWT_ALGORITHM=HS256  # Default: HS256
JWT_EXPIRATION_MINUTES=60  # Default: 30

# API
API_V1_PREFIX=/api/v1  # Default: /api/v1
DEBUG=true  # Default: false

# CORS
CORS_ORIGINS=["http://localhost:3000"]  # Default: []
```

### OAuth Variables (Optional)

Only required if using Google OAuth:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

## Environment Files

### Development (.env.local)

```bash
SCOPE=local
DATABASE_URL=sqlite+aiosqlite:///./local.db
DATABASE_ECHO=true
JWT_SECRET_KEY=dev-secret-key-not-for-production
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]
```

### Staging (.env.staging)

```bash
SCOPE=staging
DATABASE_URL=postgresql+asyncpg://user:pass@staging-db:5432/descubre_boyaca
DATABASE_ECHO=true
JWT_SECRET_KEY=${STAGING_JWT_SECRET}  # From secrets manager
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
CORS_ORIGINS=["https://staging.descubreboyaca.com"]
DEBUG=false
```

### Production (.env.prod)

```bash
SCOPE=prod
DATABASE_URL=${DATABASE_URL}  # From secrets manager
DATABASE_ECHO=false
JWT_SECRET_KEY=${JWT_SECRET}  # From secrets manager
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
CORS_ORIGINS=["https://descubreboyaca.com"]
DEBUG=false
```

## Validation

Pydantic automatically validates all settings:

### Type Validation

```python
# Type mismatch raises ValidationError
DATABASE_ECHO=not_a_boolean  # ❌ Error: not a valid boolean

# Correct
DATABASE_ECHO=true  # ✅ Converted to Python bool
```

### Required Fields

```python
# Missing required field raises ValidationError
# DATABASE_URL is required
# JWT_SECRET_KEY is required

# If not provided:
# ValidationError: field required (type=value_error.missing)
```

### Custom Validation

```python
from pydantic import field_validator


class Settings(BaseSettings):
    JWT_SECRET_KEY: str

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Validate JWT secret is strong enough."""
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        return v
```

## Best Practices

### 1. Use Environment Variables for Secrets

```python
# ❌ Bad - Secret in code
JWT_SECRET_KEY = "hardcoded-secret"

# ✅ Good - Secret from environment
JWT_SECRET_KEY: str = Field(...)  # Must come from .env
```

### 2. Provide Sensible Defaults

```python
# ✅ Good - Sensible defaults for non-sensitive values
DEBUG: bool = Field(default=False)
API_V1_PREFIX: str = Field(default="/api/v1")
```

### 3. Document Each Field

```python
# ✅ Good - Clear description
DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")
```

### 4. Use Type Hints

```python
# ✅ Good - Type safety
DEBUG: bool
CORS_ORIGINS: list[str]

# ❌ Bad - No type safety
DEBUG: Any
```

### 5. Environment-Specific Overrides

```python
# LocalSettings
DATABASE_ECHO: bool = True  # Log SQL in development

# ProdSettings
DATABASE_ECHO: bool = False  # Don't log SQL in production
```

## Testing

### Test with Monkeypatch

```python
def test_settings_from_env(monkeypatch):
    """Test settings load from environment variables."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-32-characters-min")
    monkeypatch.setenv("SCOPE", "local")

    settings = get_settings()

    assert settings.DATABASE_URL == "sqlite:///:memory:"
    assert settings.JWT_SECRET_KEY == "test-secret-key-32-characters-min"
    assert settings.SCOPE == "local"
```

### Test Validation

```python
def test_jwt_secret_validation():
    """Test JWT secret must be strong enough."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            DATABASE_URL="sqlite:///:memory:",
            JWT_SECRET_KEY="short",  # Too short
        )

    assert "at least 32 characters" in str(exc_info.value)
```

## Common Patterns

### Database URL by Environment

```python
# Local
DATABASE_URL=sqlite+aiosqlite:///./local.db

# Staging/Production
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
```

### CORS Configuration

```python
# Development - Allow localhost
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Production - Specific domains only
CORS_ORIGINS=["https://descubreboyaca.com", "https://www.descubreboyaca.com"]
```

### Feature Flags

```python
class Settings(BaseSettings):
    # Feature flags
    ENABLE_OAUTH: bool = Field(default=False)
    ENABLE_EMAIL_NOTIFICATIONS: bool = Field(default=False)

    # Check in code
    if settings.ENABLE_OAUTH:
        # Register OAuth routes
        pass
```

## Related Documentation

- [README](./README.md) - Core layer overview
- [Error Handling](./errors.md) - How errors use settings
- [Lifespan](./lifespan.md) - How lifespan uses settings
- [ARCHITECTURE.md - Section 6.2](../../../ARCHITECTURE.md#62-settings-management)
