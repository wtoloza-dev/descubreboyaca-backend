# Clients Layer

## Purpose

The `app/clients/` layer provides **database abstraction** using the **Hexagonal Architecture** pattern (Ports & Adapters). It enables the application to work with multiple database implementations (PostgreSQL, SQLite) without changing business logic.

## Architecture: Hexagonal (Ports & Adapters)

**Core Concept**: Separate the application core from external dependencies through interfaces (ports) and implementations (adapters).

```
Domain Layer (Business Logic)
        │
        │ depends on
        ▼
    Port (Interface)
        │
        │ implemented by
        ▼
    Adapters (Implementations)
        │
        ▼
    External Systems (Databases)
```

## Structure

```
app/clients/
└── sql/
    ├── ports/              # Interfaces (Contracts)
    │   ├── asynchronous.py # AsyncSQLClientPort
    │   └── synchronous.py  # SyncSQLClientPort
    │
    ├── adapters/           # Implementations
    │   ├── postgres/
    │   │   ├── asynchronous.py  # PostgreSQL async adapter
    │   │   └── synchronous.py   # PostgreSQL sync adapter
    │   └── sqlite/
    │       ├── asynchronous.py  # SQLite async adapter
    │       └── synchronous.py   # SQLite sync adapter
    │
    └── dependencies/       # Dependency injection
        ├── postgres.py     # PostgreSQL factory
        └── sqlite.py       # SQLite factory
```

## Components

This layer consists of three main components:

1. **[Ports](./ports.md)** - Interfaces defining contracts for database clients
2. **[Adapters](./adapters.md)** - Concrete implementations for specific databases
3. **[Dependencies](./adapters.md#dependencies-factories)** - Factories for creating adapter instances

## Benefits

| Benefit | Description |
|---------|-------------|
| **Swappable** | Switch databases without touching domain code |
| **Testable** | Create mock adapters for unit tests |
| **Isolated** | Database-specific code contained in adapters |
| **Flexible** | Add new databases by creating new adapters |
| **Type-safe** | Protocol-based interfaces ensure contract compliance |

## When to Use

### ✅ Use Hexagonal Architecture when:
- You need to support multiple implementations (PostgreSQL, SQLite, MySQL)
- Testing with different adapters is important
- You want to isolate external dependencies
- Framework independence is critical

### ❌ Don't use when:
- You only have one database and won't change it
- Simple CRUD with no abstraction needed
- Performance overhead of abstraction is unacceptable

## Example Flow

```
Repository (Infrastructure Layer)
    │
    │ needs session
    ▼
get_async_session_dependency() (Shared Layer)
    │
    │ uses
    ▼
AsyncSQLClientPort (Port)
    │
    │ implemented by
    ▼
AsyncPostgreSQLAdapter (Adapter)
    │
    │ connects to
    ▼
PostgreSQL Database
```

## Dependencies

**This layer depends on**:
- `app/core/settings` - For database configuration
- Standard library - No domain dependencies

**This layer is used by**:
- `app/shared/dependencies` - For session management
- `app/domains/*/infrastructure/repositories` - For data persistence

## Key Principles

1. **Ports define contracts** - Interfaces specify what adapters must implement
2. **Adapters implement details** - Database-specific code lives only in adapters
3. **Domain doesn't know adapters** - Business logic depends on ports, not implementations
4. **Dependency inversion** - High-level modules depend on abstractions, not concretions

## Documentation

- **[Ports](./ports.md)** - Detailed explanation of port interfaces
- **[Adapters](./adapters.md)** - How adapters implement ports for specific databases
- **[Adding Databases](./adding-databases.md)** - Step-by-step guide to add new database support

## Related Documentation

- [ARCHITECTURE.md - Section 3: Clients Layer](../../../ARCHITECTURE.md#3-clients-layer-hexagonal-architecture)
- [Core Layer](../core/README.md) - Framework infrastructure
- [Domains Layer](../domains/README.md) - How domains use this layer
- [Shared Layer](../shared/README.md) - Shared session dependencies
