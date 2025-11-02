"""Audit domain - Archive and audit trail management.

This domain handles archiving of deleted records and will be extended
in the future to include complete audit logging (see AUDIT_SYSTEM_PROPOSAL.md).

Current features:
- Archive soft-deleted records with metadata
- Track who deleted what and when
- Enable recovery of deleted data

Future features (planned):
- Complete audit trail for all changes (INSERT/UPDATE/DELETE)
- Field-level change tracking
- Rollback capabilities
- GDPR compliance features
"""

