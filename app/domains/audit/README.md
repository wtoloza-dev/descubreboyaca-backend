# Audit Domain

## Overview

The **Audit** domain handles archiving of deleted records and provides administrative tools for managing archived data. This domain ensures data retention, audit trails, and compliance with data management policies.

## Architecture

```
app/domains/audit/
├── domain/
│   ├── entities/
│   │   └── archive.py        # Archive entity and ArchiveData
│   └── interfaces/
│       └── archive_repository.py  # Repository interface
├── models/
│   └── archive.py             # SQLModel for database
├── repositories/
│   └── archive/
│       ├── common/
│       │   └── sql.py         # Base SQL repository
│       ├── postgresql.py      # PostgreSQL implementation
│       └── sqlite.py          # SQLite implementation
├── services/
│   └── archive.py             # Business logic
├── schemas/
│   └── admin/
│       └── hard_delete.py     # Admin schemas
├── routes/
│   └── admin/
│       └── hard_delete.py     # Admin endpoints
└── dependencies/
    └── archive.py             # Dependency injection
```

## Features

### Current Features

- ✅ **Archive deleted records**: Automatically store deleted entities with metadata
- ✅ **Track deletions**: Record who deleted what and when
- ✅ **Hard delete archives**: Admin-only permanent deletion of archive records
- ✅ **Unit of Work support**: Transaction control with `commit` parameter

### Planned Features (see project/AUDIT_SYSTEM_PROPOSAL.md)

- 🔜 Complete audit trail for all changes (INSERT/UPDATE/DELETE)
- 🔜 Field-level change tracking
- 🔜 Rollback capabilities
- 🔜 GDPR compliance features

## Entity Structure

### Archive

```python
class Archive(ArchiveData, Identity):
    """Archive entity with database identity and deletion metadata.
    
    Attributes:
        id: ULID primary key (auto-generated)
        deleted_at: Timestamp when the record was deleted (auto-generated)
        deleted_by: ULID of user who deleted the record
        original_table: Name of the source table
        original_id: ID from the original record
        data: Complete record data as dictionary
        note: Optional note or reason for deletion
    """
```

## Service Methods

### ArchiveService

```python
class ArchiveService:
    async def archive_entity(
        self,
        table_name: str,
        entity: BaseModel,
        note: str | None = None,
        deleted_by: str | None = None,
        commit: bool = True,
    ) -> Archive:
        """Archive an entity that is being deleted."""
        
    async def hard_delete_by_original_id(
        self,
        original_table: str,
        original_id: str,
    ) -> bool:
        """Hard delete an archive record (admin only)."""
        
    async def find_by_original_id(
        self,
        original_table: str,
        original_id: str,
    ) -> Archive | None:
        """Find an archive record by original table and ID."""
```

## API Endpoints

### Admin Endpoints

All endpoints require **ADMIN** role.

#### Hard Delete Archive

Permanently delete an archive record by original table and ID.

```http
DELETE /api/v1/audit/admin/archives
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "original_table": "restaurants",
  "original_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV"
}
```

**Response: 200 OK**
```json
{
  "success": true,
  "message": "Archive record from 'restaurants' with ID '01ARZ3NDEKTSV4RRFFQ69G5FAV' permanently deleted"
}
```

**Response: 200 OK (Not Found)**
```json
{
  "success": false,
  "message": "No archive found for table 'restaurants' with ID '01ARZ3NDEKTSV4RRFFQ69G5FAV'"
}
```

**Response: 401 Unauthorized**
```json
{
  "detail": "Not authenticated"
}
```

**Response: 403 Forbidden**
```json
{
  "detail": "Insufficient permissions. Admin role required."
}
```

## Usage Examples

### Archiving an Entity (Service Layer)

```python
from app.domains.audit.services import ArchiveService
from app.domains.restaurants.domain import Restaurant

# In a service method
async def delete_restaurant(self, restaurant_id: str, user_id: str) -> None:
    # Get the restaurant
    restaurant = await self.repository.find_by_id(restaurant_id)
    
    # Archive it before deleting (Unit of Work pattern)
    await self.archive_service.archive_entity(
        table_name="restaurants",
        entity=restaurant,
        note="Restaurant permanently closed",
        deleted_by=user_id,
        commit=False,  # Don't commit yet
    )
    
    # Delete the restaurant
    await self.repository.delete(restaurant_id, commit=False)
    
    # Commit both operations atomically
    await self.repository.commit()
```

### Using the Admin Endpoint

```bash
# Get admin token
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' \
  | jq -r '.access_token')

# Hard delete an archive
curl -X DELETE "http://localhost:8000/api/v1/audit/admin/archives" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "original_table": "restaurants",
    "original_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV"
  }'
```

## Database Schema

### Archive Table

```sql
CREATE TABLE archive (
    id VARCHAR(26) PRIMARY KEY,
    original_table VARCHAR(100) NOT NULL,
    original_id VARCHAR(26) NOT NULL,
    data JSON NOT NULL,
    note TEXT,
    deleted_at TIMESTAMP NOT NULL,
    deleted_by VARCHAR(26),
    INDEX idx_archive_original (original_table, original_id)
);
```

## Unit of Work Pattern

The archive service supports the Unit of Work pattern for atomic operations:

```python
# Archive and delete in a single transaction
async def delete_with_archive(self, entity_id: str, user_id: str) -> None:
    # Start transaction (implicit with session)
    
    # Archive the entity (don't commit)
    await archive_service.archive_entity(
        table_name="entities",
        entity=entity,
        deleted_by=user_id,
        commit=False,  # Important!
    )
    
    # Delete the entity (don't commit)
    await repository.delete(entity_id, commit=False)
    
    # Commit both operations together
    await repository.commit()
    
    # If anything fails, rollback is automatic
```

## Security Considerations

### Admin-Only Operations

Hard delete operations are **admin-only** and require:
- Valid JWT token
- User with `admin` role
- Authorization header in request

### Audit Trail

All archive records include:
- `deleted_at`: When the record was deleted
- `deleted_by`: Who deleted the record (ULID)
- `note`: Optional reason for deletion
- `data`: Complete snapshot of the deleted record

### GDPR Compliance

The hard delete endpoint can be used for:
- **Right to erasure**: Permanently delete user data from archives
- **Data retention**: Clean up old archived records
- **Data minimization**: Remove unnecessary archived data

## Testing

See `tests/domains/restaurants/integration/services/` for examples of:
- Archiving entities during deletion
- Unit of Work pattern usage
- Archive repository operations

## Future Enhancements

See `project/AUDIT_SYSTEM_PROPOSAL.md` for planned features including:
- Complete audit trail (INSERT/UPDATE/DELETE)
- Field-level change tracking
- Automated rollback capabilities
- Advanced compliance features

