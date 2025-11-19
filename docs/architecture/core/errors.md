# Error Handling System

## Purpose

The error handling system provides **centralized exception management**, converting domain exceptions into appropriate HTTP responses with consistent formatting and proper status codes.

## Key Concept

**Separation of Concerns**: Business logic throws domain exceptions, core layer converts them to HTTP responses.

```
Domain Layer
    │ raises
    ▼
Domain Exception
    │ caught by
    ▼
FastAPI Exception Handler (Core Layer)
    │ converts to
    ▼
HTTP JSON Response
    │ sent to
    ▼
Client
```

## Exception Hierarchy

### Base Exception

All domain exceptions inherit from a common base:

```python
# app/shared/domain/exceptions/base.py

class DomainException(Exception):
    """Base exception for all domain errors.

    Attributes:
        message: Human-readable error message
        context: Additional contextual information
        error_code: Machine-readable error identifier
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str | None = None,
    ):
        self.message = message
        self.context = context or {}
        self.error_code = error_code
        super().__init__(message)
```

### Standard Exceptions

Common exception types shared across domains:

```python
# app/shared/domain/exceptions/

class NotFoundException(DomainException):
    """Resource not found (HTTP 404)."""
    pass

class AlreadyExistsException(DomainException):
    """Resource already exists (HTTP 409)."""
    pass

class UnauthorizedException(DomainException):
    """Authentication required (HTTP 401)."""
    pass

class ForbiddenException(DomainException):
    """Insufficient permissions (HTTP 403)."""
    pass

class ValidationException(DomainException):
    """Validation error (HTTP 400)."""
    pass
```

### Domain-Specific Exceptions

Each domain defines specific exceptions:

```python
# app/domains/restaurants/domain/exceptions/restaurant.py

from app.shared.domain.exceptions import NotFoundException

class RestaurantNotFoundException(NotFoundException):
    """Raised when restaurant is not found."""

    def __init__(self, restaurant_id: str, context: dict[str, Any] | None = None):
        full_context = {
            "restaurant_id": restaurant_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Restaurant with ID '{restaurant_id}' not found",
            context=full_context,
            error_code="RESTAURANT_NOT_FOUND",
        )
```

## Exception Handlers

FastAPI exception handlers catch and convert domain exceptions.

### Handler Registration

```python
# app/core/errors/handlers.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.shared.domain.exceptions import (
    NotFoundException,
    AlreadyExistsException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with FastAPI app.

    Args:
        app: FastAPI application instance

    Example:
        >>> app = FastAPI()
        >>> register_exception_handlers(app)
    """

    @app.exception_handler(NotFoundException)
    async def not_found_handler(
        request: Request,
        exc: NotFoundException,
    ) -> JSONResponse:
        """Handle 404 Not Found exceptions.

        Args:
            request: HTTP request
            exc: Not found exception

        Returns:
            JSONResponse: 404 response with error details
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
                "context": exc.context,
            },
        )

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_handler(
        request: Request,
        exc: AlreadyExistsException,
    ) -> JSONResponse:
        """Handle 409 Conflict exceptions."""
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
                "context": exc.context,
            },
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedException,
    ) -> JSONResponse:
        """Handle 401 Unauthorized exceptions."""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exc: ForbiddenException,
    ) -> JSONResponse:
        """Handle 403 Forbidden exceptions."""
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
                "context": exc.context,
            },
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(
        request: Request,
        exc: ValidationException,
    ) -> JSONResponse:
        """Handle 400 Bad Request exceptions."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
                "error_code": exc.error_code,
                "context": exc.context,
            },
        )
```

### Pydantic Validation Errors

Handle Pydantic validation errors from request bodies:

```python
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def pydantic_validation_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """Handle Pydantic validation errors from request schemas.

    Args:
        request: HTTP request
        exc: Pydantic validation error

    Returns:
        JSONResponse: 422 Unprocessable Entity with validation errors
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "errors": exc.errors(),
        },
    )
```

## Error Flow Example

### 1. Domain Layer Raises Exception

```python
# app/domains/restaurants/application/use_cases/find_restaurant_by_id.py

from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException

class FindRestaurantByIdUseCase:
    async def execute(self, restaurant_id: str) -> Restaurant:
        restaurant = await self.repository.get_by_id(restaurant_id)

        if not restaurant:
            # Raise domain exception
            raise RestaurantNotFoundException(restaurant_id)

        return restaurant
```

### 2. Exception Propagates to Route

```python
# app/domains/restaurants/presentation/api/routes/public/find_by_id.py

@router.get("/restaurants/{restaurant_id}")
async def find_restaurant(
    restaurant_id: str,
    use_case: Annotated[FindRestaurantByIdUseCase, Depends(...)],
):
    # Exception raised here propagates to FastAPI
    restaurant = await use_case.execute(restaurant_id)
    return restaurant
```

### 3. Handler Catches and Converts

```python
# app/core/errors/handlers.py

@app.exception_handler(NotFoundException)
async def not_found_handler(request, exc):
    # Converts to HTTP 404
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Restaurant with ID '123' not found",
            "error_code": "RESTAURANT_NOT_FOUND",
            "context": {"restaurant_id": "123"},
        },
    )
```

### 4. Client Receives Response

```json
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Restaurant with ID '123' not found",
  "error_code": "RESTAURANT_NOT_FOUND",
  "context": {
    "restaurant_id": "123"
  }
}
```

## Response Format

### Success Response

```json
HTTP/1.1 200 OK

{
  "id": "01JCXYZ123",
  "name": "Restaurant Name",
  "city": "Tunja"
}
```

### Error Response

```json
HTTP/1.1 404 Not Found

{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "context": {
    "additional": "context",
    "for": "debugging"
  }
}
```

### Validation Error Response

```json
HTTP/1.1 422 Unprocessable Entity

{
  "detail": "Validation error",
  "error_code": "VALIDATION_ERROR",
  "errors": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Exception Mapping

| Exception | HTTP Status | Use Case |
|-----------|-------------|----------|
| `NotFoundException` | 404 Not Found | Resource doesn't exist |
| `AlreadyExistsException` | 409 Conflict | Duplicate resource |
| `UnauthorizedException` | 401 Unauthorized | Authentication required |
| `ForbiddenException` | 403 Forbidden | Insufficient permissions |
| `ValidationException` | 400 Bad Request | Business rule violation |
| `DomainException` | 500 Internal Server Error | Unexpected domain error |
| `ValidationError` (Pydantic) | 422 Unprocessable Entity | Invalid request format |

## Best Practices

### 1. Raise Specific Exceptions

```python
# ✅ Good - Specific exception
raise RestaurantNotFoundException(restaurant_id)

# ❌ Bad - Generic exception
raise Exception("Restaurant not found")
```

### 2. Include Context

```python
# ✅ Good - Rich context for debugging
raise RestaurantNotFoundException(
    restaurant_id,
    context={"searched_by": "name", "query": "Test Restaurant"}
)

# ❌ Bad - No context
raise RestaurantNotFoundException(restaurant_id)
```

### 3. Use Error Codes

```python
# ✅ Good - Machine-readable error code
error_code="RESTAURANT_NOT_FOUND"

# ❌ Bad - No error code
error_code=None
```

### 4. Don't Catch in Use Cases

```python
# ✅ Good - Let exception propagate
async def execute(self, restaurant_id: str) -> Restaurant:
    restaurant = await self.repository.get_by_id(restaurant_id)
    if not restaurant:
        raise RestaurantNotFoundException(restaurant_id)
    return restaurant

# ❌ Bad - Catching and returning None
async def execute(self, restaurant_id: str) -> Restaurant | None:
    try:
        restaurant = await self.repository.get_by_id(restaurant_id)
        return restaurant
    except Exception:
        return None  # Loses error information
```

## Testing

### Test Exception Raising

```python
async def test_use_case_raises_not_found(mock_repository):
    """Test use case raises exception when not found."""
    mock_repository.get_by_id.return_value = None

    use_case = FindRestaurantByIdUseCase(mock_repository)

    with pytest.raises(RestaurantNotFoundException) as exc_info:
        await use_case.execute("nonexistent")

    assert exc_info.value.error_code == "RESTAURANT_NOT_FOUND"
    assert "nonexistent" in exc_info.value.context["restaurant_id"]
```

### Test HTTP Response

```python
async def test_not_found_returns_404(client):
    """Test API returns 404 for nonexistent restaurant."""
    response = await client.get("/api/v1/restaurants/nonexistent")

    assert response.status_code == 404
    assert response.json()["error_code"] == "RESTAURANT_NOT_FOUND"
    assert "nonexistent" in response.json()["context"]["restaurant_id"]
```

## Logging

Log exceptions for monitoring and debugging:

```python
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Handle generic domain exceptions with logging."""
    logger.error(
        f"Domain exception: {exc.message}",
        extra={
            "error_code": exc.error_code,
            "context": exc.context,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error_code": exc.error_code or "INTERNAL_ERROR",
        },
    )
```

## Related Documentation

- [README](./README.md) - Core layer overview
- [Settings](./settings.md) - Configuration management
- [Lifespan](./lifespan.md) - Application lifecycle
- [ARCHITECTURE.md - Section 6.3](../../../ARCHITECTURE.md#63-error-handling-system)
