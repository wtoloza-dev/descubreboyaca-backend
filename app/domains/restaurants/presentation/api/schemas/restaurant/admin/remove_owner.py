"""Remove owner schemas.

This module contains schemas for removing an owner from a restaurant.
Corresponds to: routes/restaurant/admin/remove_owner.py

Note: DELETE operations return 204 No Content, so no request/response schemas are typically needed.
This file exists for structure consistency.
"""

from pydantic import BaseModel


class RemoveOwnerSchemaResponse(BaseModel):
    """Response schema for owner removal (admin).

    Note: This is not used in practice as DELETE returns 204 No Content.
    Defined for completeness.
    """

    pass
