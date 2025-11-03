# Database Repositories (Infrastructure Layer)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Database Repositories** | `Infrastructure Layer` | `DDD` `Repository Pattern` `Ports & Adapters` `Archive Pattern` |

## Definition

Database Repositories are **concrete implementations** of repository interfaces that handle persistence operations using specific database technologies. They act as the bridge between the domain layer (entities) and the infrastructure layer (ORM models), implementing the Repository Pattern and Ports & Adapters architecture.

## ⚠️ Important: Archive Pattern (Not Soft Delete)

**This project uses the Archive Pattern instead of soft delete:**

- ✅ **Archive Pattern**: When deleting, entities are copied to an `archive` table, then permanently deleted from their original table
- ❌ **NOT Soft Delete**: No `is_deleted` flags, no filtering of soft-deleted records
- ✅ **Unit of Work**: Archive + Delete operations are atomic (both succeed or both fail)
- ✅ **Service Layer**: Deletion logic (archive + delete) is coordinated by the Service layer, not Repository layer

**Key Implications:**
- Repository `delete()` methods perform **hard delete** (permanent removal)
- No `is_deleted` filtering in queries (deleted records don't exist)
- Service layer must archive before calling repository delete
- `commit=False` support is critical for atomic operations

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌──────────────┐         ┌─────────────────────────────┐   │
│  │   Service    │ ───────→│  Repository Interface       │   │
│  │   (Logic)    │         │      (Protocol)             │   │
│  └──────────────┘         └─────────────────────────────┘   │
└─────────────────────────────────────┬───────────────────────┘
                                      │ implements
┌─────────────────────────────────────┴───────────────────────┐
│              Infrastructure Layer (Repositories)            │
│                                                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │     repositories/entity_name/                      │     │
│  │                                                    │     │
│  │  ┌──────────────────────────────────────────────┐  │     │
│  │  │  common/sql.py                               │  │     │
│  │  │  ┌────────────────────────────────────────┐  │  │     │
│  │  │  │  SQLXxxRepository                      │  │  │     │
│  │  │  │  - Common SQL implementation           │  │  │     │
│  │  │  │  - Works across MySQL, SQLite, etc.    │  │  │     │
│  │  │  └────────────────────────────────────────┘  │  │     │
│  │  └──────────────────────────────────────────────┘  │     │
│  │                      ▲             ▲               │     │
│  │                      │             │               │     │
│  │        ┌─────────────┴─┐      ┌────┴────────────┐  │     │
│  │        │   mysql.py    │      │   sqlite.py     │  │     │
│  │        │               │      │                 │  │     │
│  │        │ MySQLXxx      │      │ SQLiteXxx       │  │     │
│  │        │ Repository    │      │ Repository      │  │     │
│  │        │               │      │                 │  │     │
│  │        │ (DB-specific  │      │ (DB-specific    │  │     │
│  │        │  overrides)   │      │  overrides)     │  │     │
│  │        └───────────────┘      └─────────────────┘  │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Three-Layer Repository Structure:**

1. **`common/sql.py`**: Base SQL implementation shared across all SQL databases
2. **`mysql.py`**: MySQL-specific implementation (inherits from common)
3. **`sqlite.py`**: SQLite-specific implementation (inherits from common)

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Repository Directory | `repositories/{entity}/` | `repositories/prompt/` |
| Common Implementation | `common/sql.py` | `repositories/prompt/common/sql.py` |
| Common Class Name | `SQL{Entity}Repository` | `SQLPromptRepository` |
| Database-Specific File | `{database}.py` | `mysql.py`, `sqlite.py` |
| Database-Specific Class | `{Database}{Entity}Repository` | `MySQLPromptRepository` |

## Directory Structure

```
repositories/
├── __init__.py                      # Export all repository implementations
├── prompt/
│   ├── __init__.py                  # Export prompt repositories
│   ├── common/
│   │   ├── __init__.py
│   │   └── sql.py                   # SQLPromptRepository (base)
│   ├── mysql.py                     # MySQLPromptRepository
│   └── sqlite.py                    # SQLitePromptRepository
├── prompt_version/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── sql.py                   # SQLPromptVersionRepository
│   ├── mysql.py                     # MySQLPromptVersionRepository
│   └── sqlite.py                    # SQLitePromptVersionRepository
└── prompt_ownership/
    ├── __init__.py
    ├── common/
    │   ├── __init__.py
    │   └── sql.py                   # SQLPromptOwnershipRepository
    ├── mysql.py                     # MySQLPromptOwnershipRepository
    └── sqlite.py                    # SQLitePromptOwnershipRepository
```

## Implementation Rules

### Common SQL Repository (Base Implementation)

**Location:** `repositories/{entity}/common/sql.py`

```python
"""Common SQL repository implementation for {Entity}.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.{domain}.domain.entities import Entity, EntityData
from app.domains.{domain}.models import EntityModel
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLEntityRepository:
    """Common SQL implementation for Entity repository.

    This repository provides async CRUD operations for Entity entities using
    SQLAlchemy/SQLModel with async/await support. It handles the conversion
    between infrastructure models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute async database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)
    - Return None when entities are not found (not exceptions)

    Note: This repository returns None when entities are not found.
    Business exceptions (NotFound, etc.) should be handled in the Service layer.

    Attributes:
        session: Async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the SQL repository with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self.session = session

    # CRUD methods here...
```

**Key Points:**
- Inherit from **nothing** (base class)
- Use `AsyncSession` for async database operations
- Import entities from domain layer, models from models layer
- All methods are `async`
- Return `None` for not found (don't raise exceptions)
- Use `AUDIT_FIELDS_EXCLUDE` when creating entities

### Database-Specific Repository

**Location:** `repositories/{entity}/mysql.py` or `sqlite.py`

```python
"""MySQL-specific implementation for Entity repository.

This module provides MySQL-specific implementation by inheriting from the
common SQL repository. Override methods here only if MySQL-specific behavior
is required (e.g., JSON operators, full-text search, etc.).
"""

from .common import SQLEntityRepository


class MySQLEntityRepository(SQLEntityRepository):
    """MySQL implementation of Entity repository.

    Inherits all CRUD operations from SQLEntityRepository. Override methods
    here only when MySQL-specific functionality is needed, such as:
    - MySQL-specific JSON operators
    - Full-text search
    - MySQL-specific optimizations
    - Custom MySQL query hints

    For standard CRUD operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLAlchemy session for database operations (inherited).
    """

    # Add MySQL-specific methods here if needed
    # Most of the time, this class will be empty (just inheriting)
```

**Key Points:**
- Inherit from `SQLEntityRepository` (from common/sql.py)
- Usually **empty** (just inheritance)
- Only add methods when database-specific behavior is needed
- `__init__` is inherited automatically

## Core Responsibilities

### 1. Entity ↔ Model Conversion

Repositories handle the conversion between domain entities and ORM models:

```
┌──────────────────────────────────────────────────────────┐
│                   Repository Flow                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Domain Entity ──────────→ ORM Model ──────────→ Database│
│  (Business Logic)     (validate)    (persist)            │
│                                                          │
│  Domain Entity ←────────── ORM Model ←────────── Database│
│  (Returned to Service) (validate)   (query)              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Conversion Pattern:**
```python
# Entity → Model (for persistence)
entity_model = EntityModel.model_validate(entity)

# Model → Entity (from database)
entity = Entity.model_validate(model)
```

### 1.1. Archive Pattern (Not Soft Delete)

This project uses an **Archive Pattern** instead of soft delete. When an entity is deleted:

```
┌──────────────────────────────────────────────────────────────────┐
│                     Archive Pattern Flow                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Get entity to delete                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  entity = await repository.get_by_id(id)                   │  │
│  │  if not entity:                                            │  │
│  │      raise NotFoundException()                             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Step 2: Create archive record (commit=False)                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  archive_data = ArchiveData(                               │  │
│  │      original_table="entities",                            │  │
│  │      original_id=entity.id,                                │  │
│  │      data=entity.model_dump(mode="json"),                  │  │
│  │      note="Deletion reason",                               │  │
│  │  )                                                         │  │
│  │  await archive_repo.create(                                │  │
│  │      archive_data, deleted_by=user_id, commit=False        │  │
│  │  )                                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Step 3: Hard delete from original table (commit=False)          │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  await repository.delete(id, commit=False)                 │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Step 4: Commit atomically (Unit of Work)                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  await uow.commit()                                        │  │
│  │  # Both archive and delete succeed together or fail together│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Key Points:**
- ✅ No `is_deleted` flags or soft delete fields
- ✅ No filtering of soft-deleted records needed
- ✅ Deleted records are physically removed from tables
- ✅ Archive table preserves complete entity data as JSON
- ✅ Uses Unit of Work for atomicity
- ✅ Archive contains: `original_table`, `original_id`, `data`, `deleted_at`, `deleted_by`, `note`

### 2. CRUD Operations

#### Find (List with Filters)
```python
async def find(
    self, filters: dict[str, Any], offset: int = 0, limit: int = 10
) -> list[Entity]:
    """Find entities by filters.

    Args:
        filters: Dictionary with column names as keys and values to filter.
        offset: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        list[Entity]: List of entities matching the filters. Empty list if none found.
    
    Note: No soft-delete filtering needed since this project uses the Archive pattern.
    Deleted records are physically removed from tables.
    """
    statement = select(EntityModel)

    # Apply filters if provided
    if filters:
        for key, value in filters.items():
            if not hasattr(EntityModel, key):
                raise ValueError(
                    f"Invalid filter field: '{key}'. "
                    f"Field does not exist in EntityModel."
                )
            statement = statement.where(getattr(EntityModel, key) == value)

    # Apply default ordering by ID (ULID has chronological ordering)
    statement = statement.order_by(desc(EntityModel.id))

    # Apply pagination
    statement = statement.offset(offset).limit(limit)

    # Execute async query
    result = await self.session.exec(statement)
    models = result.all()
    return [Entity.model_validate(model) for model in models]
```

#### Count
```python
async def count(self, filters: dict[str, Any]) -> int:
    """Count entities matching the filters.

    Args:
        filters: Dictionary with column names as keys and values to filter.

    Returns:
        int: Total number of entities matching the filters.
    
    Note: No soft-delete filtering needed since this project uses the Archive pattern.
    """
    from sqlmodel import func

    statement = select(func.count()).select_from(EntityModel)

    # Apply filters if provided
    if filters:
        for key, value in filters.items():
            if not hasattr(EntityModel, key):
                raise ValueError(
                    f"Invalid filter field: '{key}'. "
                    f"Field does not exist in EntityModel."
                )
            statement = statement.where(getattr(EntityModel, key) == value)

    # Execute query
    result = await self.session.exec(statement)
    return result.first() or 0
```

#### Get by ID
```python
async def get_by_id(self, id: str) -> Entity | None:
    """Get an entity by id.

    Args:
        id: The unique identifier of the entity.

    Returns:
        Entity | None: The entity if found, None otherwise.
    
    Note: No soft-delete filtering needed since this project uses the Archive pattern.
    """
    statement = select(EntityModel).where(EntityModel.id == id)
    result = await self.session.exec(statement)
    model = result.first()
    return Entity.model_validate(model) if model else None
```

#### Create
```python
async def create(
    self, entity_data: EntityData, created_by: str, commit: bool = True
) -> Entity:
    """Create an entity.

    Flow: EntityData → Entity (entity) → EntityModel (ORM)

    The Entity auto-generates identity and audit fields:
    - id (ULID), created_at, updated_at are auto-generated
    - created_by, updated_by are set from parameters

    Args:
        entity_data: EntityData containing business data to create.
        created_by: User identifier for audit trail.
        commit: Whether to commit the transaction.

    Returns:
        Entity: The created entity with identity and audit fields.

    Raises:
        SQLAlchemyError: If database operation fails.
    """
    # Step 1: EntityData → Entity (entity with identity + audit)
    # The Entity auto-generates: id (ULID), created_at, updated_at
    # Exclude audit fields to prevent conflicts if a full entity is passed
    entity = Entity(
        **entity_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
        created_by=created_by,
        updated_by=created_by,
    )

    # Step 2: Entity → EntityModel (ORM) using from_attributes
    entity_model = EntityModel.model_validate(entity)

    # Add to session and persist
    self.session.add(entity_model)

    if commit:
        await self.session.commit()
        await self.session.refresh(entity_model)
    else:
        await self.session.flush()  # Flush to get ID but don't commit

    # Step 3: EntityModel (ORM) → Entity to get final state from DB
    return Entity.model_validate(entity_model)
```

#### Update
```python
async def update(
    self, id: str, entity_data: EntityData, updated_by: str, commit: bool = True
) -> Entity | None:
    """Update an entity.

    Args:
        id: Unique identifier of the entity to update.
        entity_data: EntityData containing business data to update.
        updated_by: User identifier for audit trail.
        commit: Whether to commit the transaction.

    Returns:
        Entity | None: The updated entity if found, None otherwise.
    
    Note: No soft-delete filtering needed since this project uses the Archive pattern.
    """
    # Get the ORM model
    statement = select(EntityModel).where(EntityModel.id == id)
    result = await self.session.exec(statement)
    entity_model = result.first()

    if not entity_model:
        return None

    # Extract business data, excluding unset fields (partial update)
    # exclude_unset=True: only update fields that were explicitly provided
    update_data = entity_data.model_dump(exclude_unset=True)

    # Update business fields from entity
    for key, value in update_data.items():
        if hasattr(entity_model, key):
            setattr(entity_model, key, value)

    # Update audit fields
    entity_model.updated_at = datetime.now(UTC)
    entity_model.updated_by = updated_by

    self.session.add(entity_model)

    if commit:
        await self.session.commit()
        await self.session.refresh(entity_model)
    else:
        await self.session.flush()

    # Convert ORM model to domain entity
    return Entity.model_validate(entity_model)
```

#### Delete (Hard Delete with Archive)
```python
async def delete(self, id: str, commit: bool = True) -> bool:
    """Delete an entity permanently from the database.

    This project uses the Archive Pattern instead of soft delete:
    1. The entity should be archived FIRST (handled by Service layer)
    2. Then this method permanently deletes from the table
    3. Both operations are atomic (Unit of Work pattern)

    Important: This is a HARD DELETE. The Service layer is responsible
    for archiving the entity before calling this method.

    Args:
        id: The unique identifier of the entity to delete.
        commit: Whether to commit the transaction (default: True).
                Set to False when using Unit of Work pattern.

    Returns:
        bool: True if the entity was deleted, False if not found.

    Example (Service Layer):
        >>> # Step 1: Archive (commit=False)
        >>> await archive_repo.create(archive_data, deleted_by=user, commit=False)
        >>> # Step 2: Delete (commit=False)
        >>> await entity_repo.delete(id, commit=False)
        >>> # Step 3: Commit both atomically
        >>> await uow.commit()
    """
    # Get the ORM model
    statement = select(EntityModel).where(EntityModel.id == id)
    result = await self.session.exec(statement)
    entity_model = result.first()

    if not entity_model:
        return False

    # Permanently delete from database
    await self.session.delete(entity_model)

    if commit:
        await self.session.commit()
    else:
        await self.session.flush()

    return True
```

### 3. Transaction Management

```python
async def commit(self) -> None:
    """Commit the current transaction.

    Commits all pending changes in the current database session.
    """
    await self.session.commit()

async def rollback(self) -> None:
    """Rollback the current transaction.

    Rolls back all pending changes in the current database session.
    """
    await self.session.rollback()
```

## Create Flow (Detailed)

Understanding the create flow is crucial:

```
┌───────────────────────────────────────────────────────────────────┐
│                     Create Flow (3 Steps)                         │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Step 1: EntityData → Entity (with identity + audit)              │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  entity = Entity(                                           │  │
│  │      **entity_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),│  │
│  │      created_by=created_by,                                 │  │
│  │      updated_by=created_by,                                 │  │
│  │  )                                                          │  │
│  │                                                             │  │
│  │  ⚙️  Auto-generated:                                        │  │
│  │     - id (ULID)                                             │  │
│  │     - created_at (datetime.now(UTC))                        │  │
│  │     - updated_at (datetime.now(UTC))                        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  Step 2: Entity → EntityModel (ORM)                               │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  entity_model = EntityModel.model_validate(entity)          │  │
│  │  self.session.add(entity_model)                             │  │
│  │                                                             │  │
│  │  if commit:                                                 │  │
│  │      await self.session.commit()                            │  │
│  │      await self.session.refresh(entity_model)               │  │
│  │  else:                                                      │  │
│  │      await self.session.flush()  # Get ID, no commit        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  Step 3: EntityModel → Entity (return fresh from DB)              │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  return Entity.model_validate(entity_model)                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

**Why `exclude=AUDIT_FIELDS_EXCLUDE`?**

When creating an entity, we exclude audit fields from the input data to prevent conflicts:

```python
AUDIT_FIELDS_EXCLUDE = {
    "id",           # Auto-generated by Entity
    "created_at",   # Auto-generated by Entity
    "created_by",   # Set explicitly in repository
    "updated_at",   # Auto-generated by Entity
    "updated_by",   # Set explicitly in repository
    "deleted_at",   # Not used in create
    "deleted_by",   # Not used in create
    "is_deleted",   # Defaults to False
}
```

## Update Flow (Detailed)

```
┌──────────────────────────────────────────────────────────────────┐
│                     Update Flow                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Get existing model from DB                              │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  entity_model = await get_by_id(id)                        │  │
│  │  if not entity_model:                                      │  │
│  │      return None                                           │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Step 2: Apply updates (partial update support)                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  update_data = entity_data.model_dump(exclude_unset=True)  │  │
│  │                                                            │  │
│  │  for key, value in update_data.items():                    │  │
│  │      if hasattr(entity_model, key):                        │  │
│  │          setattr(entity_model, key, value)                 │  │
│  │                                                            │  │
│  │  # Update audit fields                                     │  │
│  │  entity_model.updated_at = datetime.now(UTC)               │  │
│  │  entity_model.updated_by = updated_by                      │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Step 3: Persist and return                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  self.session.add(entity_model)                            │  │
│  │  await self.session.commit()                               │  │
│  │  await self.session.refresh(entity_model)                  │  │
│  │  return Entity.model_validate(entity_model)                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Partial Updates:**

Using `exclude_unset=True` allows partial updates where only explicitly provided fields are updated:

```python
# Only update name and description
entity_data = EntityData(name="New Name", description="New Description")
# Other fields (system_prompt, user_prompt, etc.) remain unchanged
```

## Common Patterns

### Pattern 1: Basic CRUD Repository

For simple entities with standard CRUD operations.

```python
class SQLEntityRepository:
    """Common SQL implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find(self, filters: dict[str, Any], offset: int, limit: int) -> list[Entity]:
        """Find with filters and pagination."""
        ...

    async def count(self, filters: dict[str, Any]) -> int:
        """Count matching filters."""
        ...

    async def get_by_id(self, id: str) -> Entity | None:
        """Get by ID."""
        ...

    async def create(self, entity: EntityData, created_by: str, commit: bool = True) -> Entity:
        """Create entity."""
        ...

    async def update(self, id: str, entity: EntityData, updated_by: str, commit: bool = True) -> Entity | None:
        """Update entity."""
        ...

    async def delete(self, id: str, deleted_by: str, commit: bool = True) -> bool:
        """Soft delete."""
        ...

    async def hard_delete(self, id: str) -> bool:
        """Hard delete (admin only)."""
        ...

    async def commit(self) -> None:
        """Commit transaction."""
        ...

    async def rollback(self) -> None:
        """Rollback transaction."""
        ...
```

### Pattern 2: Repository with Custom Queries

For entities with domain-specific queries:

```python
class SQLPromptOwnershipRepository:
    """Ownership repository with custom queries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # Standard CRUD
    async def get_by_id(self, id: str) -> PromptOwnership | None: ...
    async def create(...) -> PromptOwnership: ...
    async def update(...) -> PromptOwnership | None: ...
    async def delete(...) -> bool: ...

    # Custom domain queries
    async def find_by_prompt_id(self, prompt_id: str) -> list[PromptOwnership]:
        """Find all ownership records for a prompt."""
        statement = (
            select(PromptOwnershipModel)
            .where(PromptOwnershipModel.prompt_id == prompt_id)
            .order_by(desc(PromptOwnershipModel.is_primary))
        )
        models = await self.session.exec(statement)
        return [PromptOwnership.model_validate(model) for model in models.all()]

    async def find_by_owner(
        self, owner_type: OwnerType, owner_id: str
    ) -> list[PromptOwnership]:
        """Find all ownership records for an owner."""
        statement = (
            select(PromptOwnershipModel)
            .where(
                PromptOwnershipModel.owner_type == owner_type.value,
                PromptOwnershipModel.owner_id == owner_id,
            )
            .order_by(desc(PromptOwnershipModel.id))
        )
        models = await self.session.exec(statement)
        return [PromptOwnership.model_validate(model) for model in models.all()]

    async def check_access(
        self, prompt_id: str, owner_type: OwnerType, owner_id: str, required_level: AccessLevel
    ) -> bool:
        """Check if owner has required access level."""
        # Business logic for access checking
        ...

    # Transactions
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
```

### Pattern 3: Repository with Complex Filters

```python
async def find(
    self,
    filters: dict[str, Any],
    offset: int = 0,
    limit: int = 10,
    order: str | None = None,
) -> list[Entity]:
    """Find with flexible ordering.
    
    Note: No soft-delete filtering needed since this project uses the Archive pattern.
    """
    statement = select(EntityModel)

    # Apply filters
    for key, value in filters.items():
        if hasattr(EntityModel, key):
            statement = statement.where(getattr(EntityModel, key) == value)

    # Apply ordering
    if order == "asc":
        statement = statement.order_by(EntityModel.created_at)
    else:  # Default to desc
        statement = statement.order_by(desc(EntityModel.created_at))

    # Apply pagination
    statement = statement.offset(offset).limit(limit)

    result = await self.session.exec(statement)
    models = result.all()

    return [Entity.model_validate(model) for model in models]
```

## Required Elements

### Common SQL Repository (`common/sql.py`)
- ✅ Module docstring explaining it's the common SQL implementation
- ✅ Import `AsyncSession` from `sqlmodel.ext.asyncio.session`
- ✅ Import domain entities from `app.domains.{domain}.domain.entities`
- ✅ Import models from `app.domains.{domain}.models`
- ✅ Import `AUDIT_FIELDS_EXCLUDE` from `app.shared.domain.constants`
- ✅ Class named `SQL{Entity}Repository`
- ✅ `__init__` accepts `AsyncSession`
- ✅ All methods are `async`
- ✅ **NO soft-delete filtering** (this project uses Archive Pattern)
- ✅ Use `AUDIT_FIELDS_EXCLUDE` in create method
- ✅ Support `commit` parameter (default `True`) in mutating operations
- ✅ Return domain entities (not ORM models)
- ✅ Return `None` for not found (not exceptions)
- ✅ Include `commit()` and `rollback()` methods
- ✅ `delete()` method performs **hard delete** (archiving handled by Service layer)

### Database-Specific Repository (`mysql.py`, `sqlite.py`)
- ✅ Module docstring explaining it's database-specific
- ✅ Import common repository: `from .common import SQL{Entity}Repository`
- ✅ Class named `{Database}{Entity}Repository`
- ✅ Inherit from `SQL{Entity}Repository`
- ✅ Usually empty (just inheritance)
- ✅ Only add methods for database-specific features

### Package `__init__.py`
- ✅ Import all repository implementations
- ✅ Export in `__all__` list

## Documentation Template

### Common SQL Repository

```python
"""Common SQL repository implementation for {Entity}.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.{domain}.domain.entities import Entity, EntityData
from app.domains.{domain}.models import EntityModel
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLEntityRepository:
    """Common SQL implementation for Entity repository.

    This repository provides async CRUD operations for Entity entities using
    SQLAlchemy/SQLModel with async/await support. It handles the conversion
    between infrastructure models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute async database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)
    - Return None when entities are not found (not exceptions)

    Note: This repository returns None when entities are not found.
    Business exceptions (NotFound, etc.) should be handled in the Service layer.

    Attributes:
        session: Async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the SQL repository with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self.session = session

    async def find(
        self, filters: dict[str, Any], offset: int = 0, limit: int = 10
    ) -> list[Entity]:
        """Find entities by filters."""
        ...

    async def count(self, filters: dict[str, Any]) -> int:
        """Count entities matching the filters."""
        ...

    async def get_by_id(self, id: str) -> Entity | None:
        """Get an entity by id."""
        ...

    async def create(
        self, entity_data: EntityData, created_by: str, commit: bool = True
    ) -> Entity:
        """Create an entity."""
        ...

    async def update(
        self, id: str, entity_data: EntityData, updated_by: str, commit: bool = True
    ) -> Entity | None:
        """Update an entity."""
        ...

    async def delete(self, id: str, deleted_by: str, commit: bool = True) -> bool:
        """Delete an entity (soft delete)."""
        ...

    async def hard_delete(self, id: str) -> bool:
        """Permanently delete an entity from storage."""
        ...

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.session.rollback()
```

### Database-Specific Repository

```python
"""MySQL-specific implementation for Entity repository.

This module provides MySQL-specific implementation by inheriting from the
common SQL repository. Override methods here only if MySQL-specific behavior
is required (e.g., JSON operators, full-text search, etc.).
"""

from .common import SQLEntityRepository


class MySQLEntityRepository(SQLEntityRepository):
    """MySQL implementation of Entity repository.

    Inherits all CRUD operations from SQLEntityRepository. Override methods
    here only when MySQL-specific functionality is needed, such as:
    - MySQL-specific JSON operators
    - Full-text search
    - MySQL-specific optimizations
    - Custom MySQL query hints

    For standard CRUD operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLAlchemy session for database operations (inherited).
    """

    # Add MySQL-specific methods here if needed
    # Example:
    # async def find_with_fulltext_search(
    #     self, search_term: str, offset: int = 0, limit: int = 10
    # ) -> list[Entity]:
    #     """Find entities using MySQL full-text search."""
    #     ...
```

## Best Practices

### 1. No Soft-Delete Filtering (Archive Pattern)

```python
# ✅ CORRECT - No soft-delete filtering needed (Archive Pattern)
statement = select(EntityModel).where(EntityModel.id == id)

# ❌ INCORRECT - Don't filter is_deleted (field doesn't exist)
statement = select(EntityModel).where(
    EntityModel.id == id,
    EntityModel.is_deleted == False,  # ❌ This field doesn't exist!
)
```

**Why?** This project uses the Archive Pattern:
- Deleted records are physically removed from tables
- A copy is saved to the `archive` table before deletion
- No `is_deleted` flags exist on entity models
- Queries naturally only return existing records

### 2. Use AUDIT_FIELDS_EXCLUDE in Create

```python
# ✅ CORRECT - Exclude audit fields
entity = Entity(
    **entity_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
    created_by=created_by,
    updated_by=created_by,
)

# ❌ INCORRECT - Don't exclude, may cause conflicts
entity = Entity(
    **entity_data.model_dump(),  # May include id, created_at, etc.
    created_by=created_by,
    updated_by=created_by,
)
```

### 3. Support Partial Updates with exclude_unset

```python
# ✅ CORRECT - Partial update support
update_data = entity_data.model_dump(exclude_unset=True)

# ❌ INCORRECT - Full update (overwrites unset fields with None)
update_data = entity_data.model_dump()
```

### 4. Return Domain Entities, Not ORM Models

```python
# ✅ CORRECT - Return domain entity
result = await self.session.exec(statement)
model = result.first()
return Entity.model_validate(model) if model else None

# ❌ INCORRECT - Return ORM model (breaks DDD)
result = await self.session.exec(statement)
return result.first()
```

### 5. Support commit Parameter for Transactions (Required for Archive Pattern)

```python
# ✅ CORRECT - Support commit parameter for Unit of Work
async def create(
    self, entity_data: EntityData, created_by: str, commit: bool = True
) -> Entity:
    # ... create logic ...
    
    if commit:
        await self.session.commit()
        await self.session.refresh(entity_model)
    else:
        await self.session.flush()  # Get ID but don't commit
    
    return Entity.model_validate(entity_model)

# ❌ INCORRECT - Always commit (breaks Archive Pattern)
async def create(self, entity_data: EntityData, created_by: str) -> Entity:
    # ... create logic ...
    await self.session.commit()  # ❌ Can't use with Unit of Work!
```

**Why?** The Archive Pattern requires:
- `commit=False` when archiving + deleting atomically
- Unit of Work manages the final commit

### 6. Archive Before Delete (Service Layer Responsibility)

```python
# ✅ CORRECT - Service coordinates Archive + Delete
async def delete_entity(self, id: str, deleted_by: str, note: str | None) -> None:
    entity = await self.repo.get_by_id(id)
    if not entity:
        raise NotFoundException()
    
    # Prepare archive data
    archive_data = ArchiveData(
        original_table="entities",
        original_id=id,
        data=entity.model_dump(mode="json"),
        note=note,
    )
    
    # Use Unit of Work for atomicity
    async with AsyncUnitOfWork(self.repo.session) as uow:
        await self.archive_repo.create(archive_data, deleted_by, commit=False)
        await self.repo.delete(id, commit=False)
        await uow.commit()  # Both succeed or both fail

# ❌ INCORRECT - Delete without archiving
async def delete_entity(self, id: str) -> None:
    await self.repo.delete(id)  # ❌ Lost data forever!
```

### 7. Validate Filter Fields

```python
# ✅ CORRECT - Validate filter fields
if filters:
    for key, value in filters.items():
        if not hasattr(EntityModel, key):
            raise ValueError(
                f"Invalid filter field: '{key}'. "
                f"Field does not exist in EntityModel."
            )
        statement = statement.where(getattr(EntityModel, key) == value)

# ❌ INCORRECT - No validation (may cause AttributeError)
for key, value in filters.items():
    statement = statement.where(getattr(EntityModel, key) == value)
```

### 8. Use Proper Ordering

```python
# ✅ CORRECT - Order by ULID (chronological) or created_at
statement = statement.order_by(desc(EntityModel.id))  # ULID
# or
statement = statement.order_by(desc(EntityModel.created_at))

# ❌ INCORRECT - No ordering (unpredictable results)
statement = select(EntityModel)
```

## Anti-Patterns (Avoid)

### ❌ Raising Exceptions for Not Found

```python
# DON'T - Raise exception in repository
async def get_by_id(self, id: str) -> Entity:
    model = result.first()
    if not model:
        raise NotFoundException(f"Entity {id} not found")  # ❌
    return Entity.model_validate(model)

# DO - Return None, let service handle
async def get_by_id(self, id: str) -> Entity | None:
    model = result.first()
    return Entity.model_validate(model) if model else None  # ✅
```

### ❌ Returning ORM Models

```python
# DON'T - Return ORM model (breaks DDD)
async def get_by_id(self, id: str) -> EntityModel | None:  # ❌
    result = await self.session.exec(statement)
    return result.first()

# DO - Return domain entity
async def get_by_id(self, id: str) -> Entity | None:  # ✅
    result = await self.session.exec(statement)
    model = result.first()
    return Entity.model_validate(model) if model else None
```

### ❌ Including Business Logic

```python
# DON'T - Business logic in repository
async def create(self, entity_data: EntityData, created_by: str) -> Entity:
    # ❌ Business validation belongs in service layer
    if entity_data.name == "forbidden":
        raise ValidationError("Name cannot be 'forbidden'")
    
    # ❌ Complex business rules belong in service layer
    if entity_data.type == "premium" and not user.is_premium:
        raise PermissionError("Premium feature")
    
    # Repository should only handle persistence
    ...

# DO - Keep repository focused on persistence
async def create(self, entity_data: EntityData, created_by: str) -> Entity:
    # Just persist the data
    entity = Entity(**entity_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE), ...)
    entity_model = EntityModel.model_validate(entity)
    self.session.add(entity_model)
    await self.session.commit()
    return Entity.model_validate(entity_model)
```

### ❌ Deleting Without Archiving

```python
# DON'T - Delete directly from repository without archiving
async def delete_entity(self, id: str) -> None:
    await self.repo.delete(id)  # ❌ Data lost forever!

# DO - Archive first, then delete (Service layer)
async def delete_entity(self, id: str, deleted_by: str) -> None:
    entity = await self.repo.get_by_id(id)
    if not entity:
        raise NotFoundException()
    
    # Create archive
    archive_data = ArchiveData(
        original_table="entities",
        original_id=id,
        data=entity.model_dump(mode="json"),
    )
    
    # Atomic archive + delete
    async with AsyncUnitOfWork(self.repo.session) as uow:
        await self.archive_repo.create(archive_data, deleted_by, commit=False)
        await self.repo.delete(id, commit=False)
        await uow.commit()  # ✅ Atomic operation
```

### ❌ Not Using AsyncSession

```python
# DON'T - Use synchronous Session
from sqlmodel import Session  # ❌

class SQLEntityRepository:
    def __init__(self, session: Session):  # ❌
        self.session = session
    
    def get_by_id(self, id: str) -> Entity | None:  # ❌ Not async
        ...

# DO - Use AsyncSession with async/await
from sqlmodel.ext.asyncio.session import AsyncSession  # ✅

class SQLEntityRepository:
    def __init__(self, session: AsyncSession):  # ✅
        self.session = session
    
    async def get_by_id(self, id: str) -> Entity | None:  # ✅ Async
        ...
```

### ❌ Not Supporting commit=False (Breaks Archive Pattern)

```python
# DON'T - Always commit in repository methods
async def delete(self, id: str) -> bool:
    entity_model = result.first()
    await self.session.delete(entity_model)
    await self.session.commit()  # ❌ Always commits, can't use in Unit of Work
    return True

# DO - Support commit parameter for transactions
async def delete(self, id: str, commit: bool = True) -> bool:
    entity_model = result.first()
    if not entity_model:
        return False
    
    await self.session.delete(entity_model)
    
    if commit:
        await self.session.commit()
    else:
        await self.session.flush()  # ✅ Allows Unit of Work coordination
    
    return True
```

**Why?** The Archive Pattern requires `commit=False` to coordinate atomic operations:
```python
async with AsyncUnitOfWork(session) as uow:
    await archive_repo.create(data, deleted_by=user, commit=False)  # Step 1
    await entity_repo.delete(id, commit=False)  # Step 2
    await uow.commit()  # Step 3: Both succeed or fail together
```

## Checklist

- [ ] Repository implements the interface (duck typing with Protocol)
- [ ] Located in `repositories/{entity}/` directory
- [ ] Common implementation in `common/sql.py` as `SQL{Entity}Repository`
- [ ] Database-specific in `{database}.py` as `{Database}{Entity}Repository`
- [ ] Uses `AsyncSession` from `sqlmodel.ext.asyncio.session`
- [ ] All methods are `async`
- [ ] Imports entities from domain layer
- [ ] Imports models from models layer
- [ ] Uses `AUDIT_FIELDS_EXCLUDE` in create
- [ ] **NO soft-delete filtering** (uses Archive Pattern)
- [ ] Returns domain entities (not ORM models)
- [ ] Returns `None` for not found (not exceptions)
- [ ] Supports `commit` parameter in mutating operations (default `True`)
- [ ] Supports partial updates with `exclude_unset=True`
- [ ] Validates filter fields
- [ ] Includes `commit()` and `rollback()` methods
- [ ] `delete()` method performs hard delete (archiving is Service layer responsibility)
- [ ] Proper docstrings for all methods
- [ ] Database-specific repository inherits from common
- [ ] Exported in package `__init__.py`

## Example: Complete Repository

See the actual implementation files for complete examples:
- **User Repository:** `app/domains/auth/repositories/user/`
  - Common: `common/sql.py` (SQLUserRepository)
  - SQLite: `sqlite.py` (UserRepositorySQLite)
  - PostgreSQL: `postgresql.py` (UserRepositoryPostgreSQL)
- **Restaurant Repository:** `app/domains/restaurants/repositories/restaurant/`
  - Common: `common/sql.py` (SQLRestaurantRepository)
  - SQLite: `sqlite.py` (RestaurantRepositorySQLite)
  - PostgreSQL: `postgresql.py` (RestaurantRepositoryPostgreSQL)
- **Archive Repository:** `app/domains/audit/repositories/archive/`
  - SQLite: `sqlite.py` (ArchiveRepositorySQLite)
  - PostgreSQL: `postgresql.py` (ArchiveRepositoryPostgreSQL)

## Related Documentation

- **Archive Pattern:** `project/AUDIT_SYSTEM_PROPOSAL.md` - Explanation of Archive vs Soft Delete
- **Unit of Work:** `app/shared/domain/patterns/unit_of_work.py` - Atomic transaction coordination
- **Repository Interfaces:** `docs/code/Repository_Interfaces.md` - Interface definitions
- **Service Layer:** `docs/code/Services.md` - How services coordinate archive + delete

