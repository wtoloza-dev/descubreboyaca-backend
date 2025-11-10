"""Hard delete archive admin endpoint.

This module provides an admin-only endpoint to permanently delete archive records.
Use with extreme caution as this operation is irreversible.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.audit.application.use_cases import (
    HardDeleteArchiveByOriginalIdUseCase,
)
from app.domains.audit.infrastructure.dependencies import (
    get_hard_delete_archive_by_original_id_use_case_dependency,
)
from app.domains.audit.presentation.api.schemas.admin import (
    HardDeleteArchiveSchemaRequest,
    HardDeleteArchiveSchemaResponse,
)
from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.users.domain import User


router = APIRouter()


@router.delete(
    path="/archives",
    status_code=status.HTTP_200_OK,
    summary="Hard delete an archive record",
    description="""
    Permanently delete an archive record by original table and ID.
    
    **Warning**: This operation is irreversible and should only be used
    for administrative purposes such as data cleanup or GDPR compliance.
    
    **Admin Only**: Requires ADMIN role.
    
    **Parameters**:
    - `original_table`: Name of the source table (e.g., "restaurants")
    - `original_id`: ULID of the original deleted record
    
    **Returns**:
    - 200 OK: Archive deleted successfully
    - 404 Not Found: No archive found for the given table and ID
    - 401 Unauthorized: Missing or invalid authentication
    - 403 Forbidden: User is not an admin
    """,
)
async def handle_hard_delete_archive(
    request: Annotated[HardDeleteArchiveSchemaRequest, Body()],
    use_case: Annotated[
        HardDeleteArchiveByOriginalIdUseCase,
        Depends(get_hard_delete_archive_by_original_id_use_case_dependency),
    ],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> HardDeleteArchiveSchemaResponse:
    """Handle hard delete archive request.

    Args:
        request: Hard delete request with table and ID
        use_case: Hard delete archive use case instance
        admin_user: Authenticated admin user (validates admin permission)

    Returns:
        HardDeleteArchiveSchemaResponse: Operation result with success status
    """
    # Execute the use case to delete the archive
    deleted = await use_case.execute(
        original_table=request.original_table,
        original_id=request.original_id,
    )

    if deleted:
        return HardDeleteArchiveSchemaResponse(
            success=True,
            message=f"Archive record from '{request.original_table}' "
            f"with ID '{request.original_id}' permanently deleted",
        )
    else:
        return HardDeleteArchiveSchemaResponse(
            success=False,
            message=f"No archive found for table '{request.original_table}' "
            f"with ID '{request.original_id}'",
        )
