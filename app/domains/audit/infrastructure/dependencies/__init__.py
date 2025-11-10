"""Audit dependency injection."""

from app.domains.audit.infrastructure.dependencies.archive import (
    get_archive_entity_use_case_dependency,
    get_archive_repository_dependency,
    get_archive_service_dependency,
    get_find_archive_by_original_id_use_case_dependency,
    get_hard_delete_archive_by_original_id_use_case_dependency,
)


__all__ = [
    # Repository
    "get_archive_repository_dependency",
    # Service (backward compatibility)
    "get_archive_service_dependency",
    # Use Cases
    "get_archive_entity_use_case_dependency",
    "get_find_archive_by_original_id_use_case_dependency",
    "get_hard_delete_archive_by_original_id_use_case_dependency",
]
