# Core Layer

## Purpose

The `app/core/` layer contains **framework-specific infrastructure** that bootstraps and configures the FastAPI application. It handles cross-cutting concerns like settings management, error handling, and application lifecycle.

## Philosophy

**Core is the foundation layer** - It provides the infrastructure that all other layers depend on, but it doesn't contain business logic.

```
┌─────────────────────────────────┐
│      FastAPI Application         │
└────────────────┬────────────────┘
                 │
                 │ uses
                 ▼
┌─────────────────────────────────┐
│          Core Layer              │
│  ┌───────────┬───────────────┐  │
│  │ Settings  │ Error Handling│  │
│  └───────────┴───────────────┘  │
└─────────────────────────────────┘
                 │
                 │ provides to
                 ▼
        ┌────────┴────────┐
        │                 │
    Domains           Clients
```

## Structure

```
app/core/
├── settings/               # Environment configuration
│   ├── __init__.py        # Exports settings instance
│   ├── base.py            # Base settings class
│   ├── local.py           # Development settings
│   ├── staging.py         # Staging settings
│   └── prod.py            # Production settings
│
├── errors/                # Global error handling
│   ├── __init__.py
│   ├── handlers.py        # FastAPI exception handlers
│   └── mappers.py         # Domain → HTTP error mapping
│
└── lifespan.py            # Application startup/shutdown
```

## Key Components

This layer consists of three main subsystems:

1. **[Settings](./settings.md)** - Environment-based configuration management
2. **[Error Handling](./errors.md)** - Domain exception to HTTP response conversion
3. **[Lifespan](./lifespan.md)** - Application startup and shutdown management

## Responsibilities

### ✅ Core Layer IS responsible for:
- Loading environment configuration
- Initializing database connections
- Registering global exception handlers
- CORS configuration
- Logging setup
- Health check endpoints
- API documentation setup

### ❌ Core Layer is NOT responsible for:
- Business logic (belongs in domains)
- Data access (belongs in domains/infrastructure)
- Request/response schemas (belongs in domains/presentation)
- Authentication logic (belongs in auth domain)

## Configuration Strategy

### Environment Variables

**Priority** (highest to lowest):
1. Environment variables
2. `.env` file
3. Default values in Settings class

**Example `.env` file**:
```bash
# Environment
SCOPE=local

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# CORS
CORS_ORIGINS=["http://localhost:3000","https://app.example.com"]
```

### Accessing Settings

**Singleton Pattern**: Settings are loaded once at startup.

```python
# ✅ Correct - Import settings instance
from app.core.settings import settings

database_url = settings.DATABASE_URL

# ❌ Wrong - Don't instantiate Settings
settings = Settings()  # Don't do this
```

## Dependencies

**This layer depends on**:
- Python standard library
- FastAPI framework
- Pydantic Settings
- Python-dotenv (for .env loading)

**This layer is used by**:
- All other layers (domains, clients, shared)
- `app/main.py` (application entry point)

## Testing Strategy

### Settings Testing

```python
def test_settings_loading(monkeypatch):
    """Test settings are loaded from environment."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")

    settings = Settings()

    assert settings.DATABASE_URL == "sqlite:///test.db"
    assert settings.JWT_SECRET_KEY == "test-secret"
```

### Error Handler Testing

```python
async def test_not_found_handler(client):
    """Test 404 error handling."""
    response = await client.get("/api/v1/restaurants/nonexistent")

    assert response.status_code == 404
    assert response.json()["error_code"] == "RESTAURANT_NOT_FOUND"
```

## Key Principles

1. **Single Source of Truth** - All configuration in one place
2. **Environment-Based** - Different settings per environment
3. **Type-Safe** - Pydantic validates configuration
4. **Centralized Error Handling** - Domain exceptions mapped consistently
5. **Lifecycle Management** - Clean startup/shutdown

## Documentation

- **[Settings](./settings.md)** - Environment configuration and management
- **[Error Handling](./errors.md)** - Exception handling and HTTP mapping
- **[Lifespan](./lifespan.md)** - Application lifecycle management

## Related Documentation

- [ARCHITECTURE.md - Section 6: Core Infrastructure](../../../ARCHITECTURE.md#6-core-infrastructure)
- [Clients Layer](../clients/README.md) - Database client initialization
- [Domains Layer](../domains/README.md) - How domains use settings
- [Shared Layer](../shared/README.md) - Shared dependencies
