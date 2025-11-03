"""Dish delete schemas for admin.

This module contains response schema for the admin delete route.
Corresponds to: routes/dish/admin/delete.py

Note: DELETE operations return 204 No Content, so no response schema is used in practice.
This file exists for structure consistency.
"""

from pydantic import BaseModel


class DeleteDishSchemaResponse(BaseModel):
    """Response schema for dish deletion (admin).

    Note: This is not used in practice as DELETE returns 204 No Content.
    Defined for completeness and potential future use.
    """

    pass
