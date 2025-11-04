"""Hard delete archive schemas.

This module defines request and response schemas for permanently deleting
archive records. This is an admin-only operation.
"""

from pydantic import BaseModel, ConfigDict, Field


class HardDeleteArchiveSchemaRequest(BaseModel):
    """Request schema for hard deleting an archive record.

    Attributes:
        original_table: Name of the source table (e.g., "restaurants")
        original_id: ID from the original deleted record
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "original_table": "restaurants",
                    "original_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                }
            ]
        }
    )

    original_table: str = Field(
        ...,
        description="Name of the source table",
        min_length=1,
        max_length=100,
        examples=["restaurants", "dishes", "users"],
    )
    original_id: str = Field(
        ...,
        description="ULID of the original deleted record",
        min_length=26,
        max_length=26,
        examples=["01ARZ3NDEKTSV4RRFFQ69G5FAV"],
    )


class HardDeleteArchiveSchemaResponse(BaseModel):
    """Response schema for hard delete archive operation.

    Attributes:
        success: Whether the operation was successful
        message: Descriptive message about the operation result
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "success": True,
                    "message": "Archive record permanently deleted",
                }
            ]
        }
    )

    success: bool = Field(
        ...,
        description="Whether the archive was successfully deleted",
        examples=[True, False],
    )
    message: str = Field(
        ...,
        description="Result message",
        examples=[
            "Archive record permanently deleted",
            "Archive record not found",
        ],
    )
