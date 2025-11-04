"""Delete user schemas for admin operations."""

from pydantic import BaseModel, ConfigDict, Field


class DeleteUserSchemaRequest(BaseModel):
    """Schema for deleting a user (admin operation).

    This follows the archive pattern - the user will be soft-deleted
    and their data archived for audit purposes.

    Attributes:
        note: Optional note explaining why the user was deleted
    """

    model_config = ConfigDict(
        json_schema_extra={"example": {"note": "User requested account deletion"}}
    )

    note: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional note explaining the deletion reason",
        examples=["User violated terms of service", "Duplicate account"],
    )
