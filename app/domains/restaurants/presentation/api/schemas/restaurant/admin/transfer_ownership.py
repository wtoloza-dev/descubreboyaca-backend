"""Transfer ownership schemas.

This module contains schemas for transferring primary ownership.
Corresponds to: routes/restaurant/admin/transfer_ownership.py

Note: POST operation with path parameters only, no request body needed.
"""

from pydantic import BaseModel

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    OwnershipSchemaResponse,
)


class TransferOwnershipSchemaResponse(BaseModel):
    """Response schema for ownership transfer.

    Returns the updated ownership record after transfer.
    """

    # The response is the updated OwnershipSchemaResponse
    pass


# Re-export common schema as the actual response
__all__ = ["OwnershipSchemaResponse"]
