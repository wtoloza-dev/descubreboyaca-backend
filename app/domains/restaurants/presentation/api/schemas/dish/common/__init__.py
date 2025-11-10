"""Common dish schemas shared across admin, owner, and public endpoints."""

from .base import CreateDishSchemaRequest, UpdateDishSchemaRequest


__all__ = [
    "CreateDishSchemaRequest",
    "UpdateDishSchemaRequest",
]
