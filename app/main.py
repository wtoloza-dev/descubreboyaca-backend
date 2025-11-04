"""Main FastAPI application entry point.

This module initializes and configures the FastAPI application with all
required middleware, routers, and settings using the Application Factory pattern.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.lifespan import lifespan
from app.core.routes import router as core_router
from app.core.settings import settings
from app.domains.audit.routes import router as audit_router
from app.domains.auth.routes import router as auth_router
from app.domains.favorites.routes import router as favorites_router
from app.domains.restaurants.routes import router as restaurants_router
from app.domains.reviews.routes import router as reviews_router
from app.domains.users.routes.admin import router as users_admin_router


def register_routers(app: FastAPI) -> None:
    """Register all application routers.

    This function registers all application routers with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Core routers
    app.include_router(core_router, include_in_schema=settings.DEBUG)
    app.include_router(auth_router)

    # API v1 routers
    api_v1_router = APIRouter(prefix="/api/v1")
    api_v1_router.include_router(restaurants_router)
    api_v1_router.include_router(favorites_router)
    api_v1_router.include_router(reviews_router)
    api_v1_router.include_router(users_admin_router, prefix="/users", tags=["Users"])
    api_v1_router.include_router(audit_router)
    app.include_router(api_v1_router)


def register_cors(app: FastAPI) -> None:
    """Register CORS middleware with the FastAPI application.

    This function registers the CORS middleware with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    This function implements the Application Factory pattern, allowing for
    better testability and flexibility in configuration.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME + " " + settings.SCOPE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION + " " + settings.SCOPE,
        redirect_slashes=True,  # Redirige /endpoint/ a /endpoint y viceversa
        lifespan=lifespan,  # Manage database lifecycle
    )

    # Register CORS middleware
    register_cors(app)

    # Register exception handlers
    # register_exception_handlers(app)

    # Register all routers
    register_routers(app)

    return app


# Create application instance for FastAPI CLI and uvicorn
app = create_app()
