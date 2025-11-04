# Testing Architecture

## Table of Contents

1. [Overview](#overview)
2. [Testing Levels](#testing-levels)
3. [Testing Philosophy: Functional vs Implementation](#testing-philosophy-functional-vs-implementation)
4. [Directory Structure](#directory-structure)
5. [File Organization Principle: One File = One Test Class](#file-organization-principle-one-file--one-test-class)
6. [Naming Conventions](#naming-conventions)
7. [Documentation Patterns](#documentation-patterns)
8. [Test Structure (AAA Pattern)](#test-structure-aaa-pattern)
9. [Fixtures and Setup](#fixtures-and-setup)
10. [What to Test at Each Level](#what-to-test-at-each-level)
11. [Best Practices](#best-practices)
12. [Examples](#examples)

---

## Overview

This document defines the testing architecture for the DescubreBoyaca backend application. Our testing strategy follows a three-tier approach that mirrors the application's layered architecture, ensuring comprehensive coverage from HTTP endpoints down to domain logic.

### Testing Philosophy

- **Mirror Application Structure**: Test organization reflects the app's architecture
- **Progressive Complexity**: Tests range from simple unit tests to complex E2E scenarios
- **Clarity Over Cleverness**: Readable, maintainable tests are prioritized
- **Fast Feedback**: Tests execute quickly (entire suite < 2 seconds)
- **Isolation**: Each test is independent and can run in any order

---

## Testing Levels

### 1. E2E Tests (End-to-End)
**Purpose**: Test complete user flows through HTTP endpoints

- **Scope**: HTTP Request → Route → Service → Repository → Database → Response
- **Speed**: Slowest (~0.68s for 20 tests)
- **What**: User-facing functionality, API contracts
- **Tools**: `TestClient`, fixtures, real database transactions

### 2. Integration Tests
**Purpose**: Test component interactions with dependencies

- **Scope**: Service/Repository → Database
- **Speed**: Medium (~0.81s for 22 tests)
- **What**: Business logic, data access patterns, queries
- **Tools**: Direct service/repository instantiation, test database

### 3. Unit Tests
**Purpose**: Test isolated domain logic without dependencies

- **Scope**: Entities, Value Objects, Validators
- **Speed**: Fastest (~0.02s for 9 tests)
- **What**: Validation rules, business rules, transformations
- **Tools**: Pure Python, Pydantic validators

---

## Testing Philosophy: Functional vs Implementation

### What is Functional Testing?

**Functional Testing** focuses on **WHAT** the system does (behavior) rather than **HOW** it does it (implementation). This is an important distinction that often causes confusion.

### Two Perspectives on Testing

#### Perspective 1: Scope (Horizontal Axis)

This is the traditional test pyramid based on **scope**:

```
        ┌─────────┐
        │   E2E   │  ← Broadest scope (full system)
        ├─────────┤
        │  Integ  │  ← Medium scope (multiple components)
        ├─────────┤
        │  Unit   │  ← Narrowest scope (single unit)
        └─────────┘
```

#### Perspective 2: Knowledge (Vertical Axis)

Tests can also be categorized by **how much they know** about implementation:

```
┌──────────────────────────────────────┐
│     FUNCTIONAL (Black-box)           │  ← Knows inputs/outputs only
│     "What does it do?"               │
├──────────────────────────────────────┤
│     MIX (Gray-box)                   │  ← Knows some internals
│                                      │
├──────────────────────────────────────┤
│     IMPLEMENTATION (White-box)       │  ← Knows all internals
│     "How does it work?"              │
└──────────────────────────────────────┘
```

**Functional (Black-box) Tests**:
- Test behavior without knowing implementation
- Focus on inputs → outputs
- Don't care about internal classes/methods
- Can survive refactoring

**Implementation (White-box) Tests**:
- Test specific implementation details
- Know about internal structure
- Verify algorithms, data structures
- May break during refactoring

### How This Maps to Our 3-Level Architecture

Our testing architecture naturally incorporates **both perspectives**:

```
┌─────────────────────────────────────────────────────────┐
│              FUNCTIONAL (Black-box)                      │
│              "Can users do X?"                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  E2E Tests (20 tests)                                   │
│  • Tests complete user workflows                        │
│  • Doesn't know about services/repositories             │
│  • Only knows HTTP requests/responses                   │
│                                                          │
│  Example:                                               │
│    def test_get_restaurant(test_client):                │
│        response = test_client.get("/restaurants/123")   │
│        assert response.status_code == 200               │
│        # Don't know/care how it fetches from DB         │
│                                                          │
├─────────────────────────────────────────────────────────┤
│              MIX (Gray-box)                              │
│              "Do components work together?"             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Integration Tests (22 tests)                           │
│  • Tests component interactions                         │
│  • Knows about services/repositories                    │
│  • Partially knows implementation                       │
│                                                          │
│  Example (Functional):                                  │
│    def test_service_filters_by_city(session):          │
│        service = RestaurantService(...)                 │
│        results = await service.find(city="Tunja")       │
│        assert len(results) == 2                         │
│        # Don't care about SQL query details             │
│                                                          │
│  Example (Implementation):                              │
│    def test_repository_applies_where_clause(session):   │
│        repo = RestaurantRepositorySQLite(session)       │
│        results = await repo.find(filters={"city": "X"}) │
│        # Knows it uses SQLAlchemy WHERE clause          │
│                                                          │
├─────────────────────────────────────────────────────────┤
│              IMPLEMENTATION (White-box)                  │
│              "Does validation logic work?"              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Unit Tests (9 tests)                                   │
│  • Tests isolated domain logic                          │
│  • Knows exact validation rules                         │
│  • Tests specific algorithms                            │
│                                                          │
│  Example:                                               │
│    def test_price_level_rejects_invalid():             │
│        with pytest.raises(ValidationError):             │
│            RestaurantData(price_level=5)                │
│        # Knows price_level range is 1-4                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Do We Need a Separate "Functional Test" Level?

**No.** Here's why:

1. **E2E tests ARE functional tests**: They already test behavior from a user perspective
2. **Not a different scope**: Functional vs Implementation is a perspective, not a scope level
3. **Avoids duplication**: Adding "Functional" as a 4th level would duplicate E2E tests
4. **Industry standard**: Most modern architectures use the 3-level pyramid (Unit → Integration → E2E)

### Testing Terminology Equivalents

Different communities use different terms for similar concepts. Here's how common terminology maps to our architecture:

| Common Term | Our Equivalent | Description |
|-------------|---------------|-------------|
| **Functional Tests** | E2E Tests | Tests behavior from user perspective |
| **Acceptance Tests** | E2E Tests | Tests acceptance criteria (user stories) |
| **System Tests** | E2E Tests | Tests entire system working together |
| **API Tests** | E2E Tests | Tests REST API endpoints |
| **Component Tests** | Integration Tests | Tests individual components |
| **Service Tests** | Integration Tests | Tests service layer |
| **Contract Tests** | N/A | For microservices (not applicable here) |
| **Smoke Tests** | Subset of E2E | Critical path tests only |
| **Regression Tests** | All Levels | Tests that prevent bugs from returning |

### Key Takeaway

Our **3-level architecture** is complete and follows industry best practices:

1. **Unit Tests** → Test isolated logic (implementation focus)
2. **Integration Tests** → Test component interactions (mixed perspective)
3. **E2E Tests** → Test complete workflows (functional focus)

We use "E2E" terminology to emphasize the complete **request → database → response** cycle, but these tests are inherently **functional** because they test system behavior without knowing implementation details.

---

## Directory Structure

The test structure **mirrors** the application structure:

```
tests/
├── conftest.py                        # Global fixtures (database, client)
├── ARCHITECTURE.md                    # This document
│
└── domains/
    └── {domain_name}/                 # e.g., restaurants, auth
        ├── conftest.py                # Domain-specific fixtures
        │
        ├── e2e/                       # End-to-End tests
        │   ├── public/                # Maps to app/domains/{domain}/routes/public/
        │   │   ├── test_get.py        # Maps to routes/public/get.py
        │   │   ├── test_list.py       # Maps to routes/public/list.py
        │   │   └── test_list_by_city.py
        │   ├── owner/                 # Maps to app/domains/{domain}/routes/owner/
        │   │   └── test_*.py
        │   └── admin/                 # Maps to app/domains/{domain}/routes/admin/
        │       ├── test_create.py
        │       └── test_delete.py
        │
        ├── integration/               # Integration tests
        │   ├── services/              # Maps to app/domains/{domain}/services/
        │   │   ├── test_{service_name}_get.py      # ONE operation per file
        │   │   ├── test_{service_name}_list.py     # ONE operation per file
        │   │   └── test_{service_name}_delete.py   # ONE operation per file
        │   └── repositories/          # Maps to app/domains/{domain}/repositories/
        │       ├── test_{repository_name}_get.py   # ONE operation per file
        │       ├── test_{repository_name}_find.py  # ONE operation per file
        │       └── test_{repository_name}_count.py # ONE operation per file
        │
        └── unit/                      # Unit tests
            ├── entities/              # Maps to app/domains/{domain}/domain/entities/
            │   └── test_{entity_name}.py
            ├── value_objects/         # Maps to app/domains/{domain}/domain/value_objects/
            │   └── test_{vo_name}.py
            └── exceptions/            # Maps to app/domains/{domain}/domain/exceptions/
                └── test_{exception_name}.py
```

### Mapping to Application Structure

```
app/domains/restaurants/routes/public/get.py
    ↓
tests/domains/restaurants/e2e/public/test_get.py

app/domains/restaurants/services/restaurant.py (get_restaurant_by_id method)
    ↓
tests/domains/restaurants/integration/services/test_restaurant_service_get.py

app/domains/restaurants/services/restaurant.py (find_restaurants method)
    ↓
tests/domains/restaurants/integration/services/test_restaurant_service_list.py

app/domains/restaurants/services/restaurant.py (delete_restaurant method)
    ↓
tests/domains/restaurants/integration/services/test_restaurant_service_delete.py

app/domains/restaurants/domain/entities/restaurant.py
    ↓
tests/domains/restaurants/unit/entities/test_restaurant.py
```

---

## File Organization Principle: One File = One Test Class

### Core Rule

**Each test file MUST contain exactly ONE test class (or a small group of VERY closely related classes).**

This principle ensures:
- ✅ **Easy navigation**: File name tells you exactly what's inside
- ✅ **Focused testing**: Each file has a single responsibility
- ✅ **Manageable size**: Files stay small (~50-100 lines)
- ✅ **Clear intent**: No ambiguity about what's being tested

### Why This Matters

#### ❌ **BAD** - Multiple unrelated classes in one file:

```python
# tests/integration/services/test_restaurant_service.py (415 lines)
class TestRestaurantServiceGet:           # 50 lines
    # Tests for get operations
    
class TestRestaurantServiceList:          # 100 lines  
    # Tests for list operations
    
class TestRestaurantServiceCreate:        # 80 lines
    # Tests for create operations
    
class TestRestaurantServiceUpdate:        # 85 lines
    # Tests for update operations
    
class TestRestaurantServiceDelete:        # 100 lines
    # Tests for delete operations
```

**Problems:**
- 😵 415 lines - hard to navigate
- 🔍 Need to scroll to find specific tests
- 📝 Git diffs affect unrelated tests
- 🤷 File name doesn't indicate which operation

#### ✅ **GOOD** - One class per file:

```python
# tests/integration/services/test_restaurant_service_get.py (~70 lines)
class TestRestaurantServiceGet:
    """Integration tests for RestaurantService get operations."""
    # All get-related tests here

# tests/integration/services/test_restaurant_service_list.py (~120 lines)
class TestRestaurantServiceList:
    """Integration tests for RestaurantService list operations."""
    # All list-related tests here

# tests/integration/services/test_restaurant_service_delete.py (~250 lines)
class TestRestaurantServiceDeleteSuccess:
    """Tests for successful delete operations."""
    
class TestRestaurantServiceDeleteAtomicity:
    """Tests for delete atomicity and rollback."""
    
class TestRestaurantServiceDeleteValidation:
    """Tests for delete validation."""
    # Multiple CLOSELY RELATED classes allowed for complex operations
```

**Benefits:**
- 👍 Each file ~70-120 lines - easy to read
- 🔍 File name = operation being tested
- 📝 Changes are isolated
- 🎯 Clear purpose and scope

### Naming Pattern for Split Files

When splitting service/repository tests by operation:

```
Component                    Method              →  Test File Name
────────────────────────────────────────────────────────────────────────────
RestaurantService            get_by_id()         →  test_restaurant_service_get.py
RestaurantService            find_restaurants()  →  test_restaurant_service_list.py
RestaurantService            delete_restaurant() →  test_restaurant_service_delete.py
RestaurantRepository         get_by_id()         →  test_restaurant_repository_get.py
RestaurantRepository         find()              →  test_restaurant_repository_find.py
RestaurantRepository         count()             →  test_restaurant_repository_count.py
RestaurantRepository         create()            →  test_restaurant_repository_create.py
```

### Exception: Multiple Related Classes Allowed

For **complex operations** (like DELETE with Unit of Work), multiple related classes in one file are acceptable:

```python
# test_restaurant_service_delete.py
class TestRestaurantServiceDeleteSuccess:
    """Tests for successful delete scenarios."""
    
class TestRestaurantServiceDeleteAtomicity:
    """Tests for transaction rollback on failures."""
    
class TestRestaurantServiceDeleteValidation:
    """Tests for input validation."""
```

**Key**: All classes test the SAME operation from different angles.

### Real-World Example

**Restaurant Integration Tests Structure:**

```
tests/domains/restaurants/integration/
├── services/
│   ├── test_restaurant_service_get.py      (2 tests)  ← GET operations only
│   ├── test_restaurant_service_list.py     (4 tests)  ← LIST/COUNT operations
│   └── test_restaurant_service_delete.py   (6 tests)  ← DELETE operations (3 classes)
│
└── repositories/
    ├── test_restaurant_repository_get.py           (2 tests)  ← GET operations only
    ├── test_restaurant_repository_create.py        (1 test)   ← CREATE operations only
    ├── test_restaurant_repository_find.py          (6 tests)  ← FIND operations only
    ├── test_restaurant_repository_count.py         (4 tests)  ← COUNT operations only
    └── test_restaurant_repository_special_cases.py (3 tests)  ← Edge cases
```

**Result:**
- 🎯 28 tests in 8 well-organized files
- 📏 Average ~70-80 lines per file
- 🔍 Instant lookup: "Where are COUNT tests?" → `test_restaurant_repository_count.py`

---

## Naming Conventions

### File Names

```python
# E2E Tests - match route file names
app/domains/restaurants/routes/public/get.py
  → tests/domains/restaurants/e2e/public/test_get.py

app/domains/restaurants/routes/owner/create.py
  → tests/domains/restaurants/e2e/owner/test_create.py

# Integration Tests - SPLIT BY OPERATION (one file per method/operation)
app/domains/restaurants/services/restaurant.py (get_restaurant_by_id method)
  → tests/domains/restaurants/integration/services/test_restaurant_service_get.py

app/domains/restaurants/services/restaurant.py (find_restaurants + count_restaurants methods)
  → tests/domains/restaurants/integration/services/test_restaurant_service_list.py

app/domains/restaurants/services/restaurant.py (delete_restaurant method)
  → tests/domains/restaurants/integration/services/test_restaurant_service_delete.py

app/domains/restaurants/repositories/restaurant/sqlite.py (get_by_id method)
  → tests/domains/restaurants/integration/repositories/test_restaurant_repository_get.py

app/domains/restaurants/repositories/restaurant/sqlite.py (find method)
  → tests/domains/restaurants/integration/repositories/test_restaurant_repository_find.py

app/domains/restaurants/repositories/restaurant/sqlite.py (count method)
  → tests/domains/restaurants/integration/repositories/test_restaurant_repository_count.py

# Unit Tests - match entity/value object names
app/domains/restaurants/domain/entities/restaurant.py
  → tests/domains/restaurants/unit/entities/test_restaurant.py
```

### Test Class Names

Group related tests using descriptive class names:

```python
# E2E: Describe the endpoint/feature being tested
class TestGetRestaurant:
    """Tests for GET /restaurants/{id} endpoint."""

class TestListRestaurants:
    """Tests for GET /restaurants endpoint."""

# Integration: Describe the component and operation
class TestRestaurantServiceGet:
    """Integration tests for RestaurantService get operations."""

class TestRestaurantRepositoryCreate:
    """Integration tests for RestaurantRepository create operations."""

# Unit: Describe the entity/component being tested
class TestRestaurantData:
    """Unit tests for RestaurantData validation."""

class TestRestaurant:
    """Unit tests for Restaurant entity."""
```

### Test Function Names

Use descriptive names that explain the scenario:

```python
# Pattern: test_{action}_{scenario}_{expected_result}

# Good examples
def test_get_existing_restaurant()
def test_get_nonexistent_restaurant()
def test_list_with_pagination()
def test_list_filter_by_city()
def test_create_restaurant_data_with_invalid_name_empty()

# Avoid
def test_get()           # Too vague
def test_1()             # No context
def test_restaurant()    # What about it?
```

---

## Documentation Patterns

### Dual Documentation Strategy

Every test MUST include **both**:
1. **Given-When-Then** docstring (for Product/QA/Business)
2. **AAA comments** in code (for Developers)

### Given-When-Then (Docstring)

**Purpose**: Explain the test scenario in business terms

```python
def test_example(self):
    """Short description of what is being tested.
    
    Given: The preconditions or initial state
    When: The action being performed
    Then: The expected outcome
    """
```

**Example**:

```python
def test_get_restaurant_by_id_existing(self, test_session, create_test_restaurant):
    """Test getting an existing restaurant through service.
    
    Given: A restaurant exists in database
    When: Calling service.get_restaurant_by_id()
    Then: Returns restaurant entity
    """
```

### Key Points:
- **Given**: Setup, preconditions, test data
- **When**: The specific action being tested
- **Then**: Expected results, side effects

---

## Test Structure (AAA Pattern)

### Arrange-Act-Assert (Code Comments)

**Purpose**: Structure test code for developer readability

```python
def test_example(self):
    """Given-When-Then docstring here."""
    
    # Arrange
    # Setup: Create test data, instantiate objects, configure state
    
    # Act
    # Execute: Call the function/method being tested
    
    # Assert
    # Verify: Check results, state changes, exceptions
```

**Complete Example**:

```python
@pytest.mark.asyncio
async def test_get_restaurant_by_id_existing(
    self, test_session: AsyncSession, create_test_restaurant
):
    """Test getting an existing restaurant through service.
    
    Given: A restaurant exists in database
    When: Calling service.get_restaurant_by_id()
    Then: Returns restaurant entity
    """
    # Arrange
    restaurant_repo = RestaurantRepositorySQLite(test_session)
    archive_repo = ArchiveRepositorySQLite(test_session)
    service = RestaurantService(restaurant_repo, archive_repo)
    created = await create_test_restaurant(name="Test Restaurant")
    
    # Act
    result = await service.get_restaurant_by_id(created.id)
    
    # Assert
    assert result.id == created.id
    assert result.name == "Test Restaurant"
```

### Why Both Patterns?

| Pattern | Audience | Purpose |
|---------|----------|---------|
| **Given-When-Then** | PM, QA, Business | Understand what scenario is being tested |
| **AAA Comments** | Developers | Navigate and modify test code quickly |

---

## Fixtures and Setup

### Global Fixtures (`tests/conftest.py`)

These fixtures are available to **all tests**:

```python
@pytest.fixture(name="test_engine", scope="function")
async def fixture_test_engine():
    """Async SQLite engine with temporary file database."""
    # Creates isolated database for each test
    
@pytest.fixture(name="test_session", scope="function")
async def fixture_test_session(test_engine):
    """Async session for database operations."""
    # Provides clean session for each test
    
@pytest.fixture(name="test_client")
def fixture_test_client(test_session):
    """FastAPI TestClient with dependency overrides."""
    # Provides HTTP client with test database
```

### Domain Fixtures (`tests/domains/{domain}/conftest.py`)

Domain-specific fixtures for creating test data:

```python
@pytest.fixture(name="create_test_restaurant")
def fixture_create_test_restaurant(test_session: AsyncSession):
    """Factory fixture for creating test restaurants."""
    
    async def _create(**kwargs):
        restaurant = RestaurantModel(
            id=kwargs.get("id", generate_ulid()),
            name=kwargs.get("name", "Test Restaurant"),
            # ... default values with kwargs overrides
        )
        test_session.add(restaurant)
        await test_session.commit()
        await test_session.refresh(restaurant)
        return restaurant
        
    return _create
```

### Fixture Scope

- `scope="function"` (default): New instance per test (database, session)
- `scope="module"`: Shared across all tests in a file
- `scope="session"`: Shared across entire test run

**Rule**: Use `function` scope for database fixtures to ensure test isolation.

---

## What to Test at Each Level

### E2E Tests (Route Layer)

**Test the HTTP contract:**

✅ **DO Test:**
- HTTP status codes (200, 201, 404, 422, etc.)
- Response body structure and data
- Request validation (query params, path params, body)
- Authentication/authorization
- Pagination (offset, limit, total)
- Filters and query combinations
- Error responses

❌ **DON'T Test:**
- Internal service logic (that's integration)
- Database queries directly (use the API)
- Edge cases of validation rules (that's unit)

**Example Structure:**

```python
class TestGetRestaurant:
    """E2E tests for GET /restaurants/{id}."""
    
    def test_get_existing_restaurant(self):
        """Test successful retrieval with 200."""
        
    def test_get_nonexistent_restaurant(self):
        """Test 404 for missing resource."""
        
    def test_get_with_invalid_id_format(self):
        """Test 422 for malformed ULID."""
        
    def test_get_restaurant_includes_all_fields(self):
        """Test complete response schema."""
```

### Integration Tests (Service/Repository Layer)

**Test component interactions:**

✅ **DO Test:**
- Service business logic
- Repository queries and filters
- Data persistence and retrieval
- Error handling and exceptions
- Transaction behavior
- Aggregate operations (count, sum, etc.)

❌ **DON'T Test:**
- HTTP/routing logic (that's E2E)
- Pure validation (that's unit)
- External APIs (use mocks)

**Example Structure:**

```python
class TestRestaurantServiceGet:
    """Integration tests for RestaurantService get operations."""
    
    async def test_get_restaurant_by_id_existing(self):
        """Test service returns entity for existing ID."""
        
    async def test_get_restaurant_by_id_not_found(self):
        """Test service raises exception for missing ID."""

class TestRestaurantRepositoryFind:
    """Integration tests for RestaurantRepository find operations."""
    
    async def test_find_with_city_filter(self):
        """Test repository applies city filter correctly."""
        
    async def test_find_with_pagination(self):
        """Test repository respects offset and limit."""
```

### Unit Tests (Domain Layer)

**Test isolated logic:**

✅ **DO Test:**
- Entity validation rules
- Value object constraints
- Domain exceptions
- Business rule calculations
- Data transformations (e.g., `model_dump(mode="json")`)

❌ **DON'T Test:**
- Database operations
- HTTP endpoints
- Service orchestration

**Example Structure:**

```python
class TestRestaurantData:
    """Unit tests for RestaurantData validation."""
    
    def test_create_restaurant_data_with_valid_minimal_data(self):
        """Test entity accepts minimum required fields."""
        
    def test_create_restaurant_data_with_invalid_name_empty(self):
        """Test entity rejects empty name."""
        
    def test_create_restaurant_data_with_invalid_price_level_too_high(self):
        """Test entity enforces price level range."""

class TestRestaurant:
    """Unit tests for Restaurant entity."""
    
    def test_restaurant_model_dump_mode_json_converts_http_url(self):
        """Test HttpUrl serializes as string in JSON mode."""
```

---

## Best Practices

### 1. Test Isolation

Each test MUST be independent:

```python
# ✅ Good - creates its own data
async def test_example(self, test_session, create_test_restaurant):
    restaurant = await create_test_restaurant(name="Test")
    # test uses only this restaurant

# ❌ Bad - depends on data from other tests
async def test_example(self, test_session):
    # assumes restaurant with ID "123" exists
    restaurant = await get_by_id("123")
```

### 2. Descriptive Assertions

```python
# ✅ Good - clear what's being checked
assert result.name == "Expected Name"
assert result.city == "Tunja"
assert len(results) == 3

# ❌ Bad - unclear what failed
assert result
assert data["data"]
```

### 3. One Concept Per Test

```python
# ✅ Good - tests one scenario
def test_list_filter_by_city(self):
    """Test filtering restaurants by city."""
    # Only tests city filter

def test_list_filter_by_price_level(self):
    """Test filtering restaurants by price level."""
    # Only tests price filter

# ❌ Bad - tests multiple scenarios
def test_list_filters(self):
    """Test all possible filters."""
    # Tests city, price, cuisine, features...
```

### 4. Async/Await Consistency

```python
# ✅ Good - async test for async code
@pytest.mark.asyncio
async def test_get_restaurant(self):
    result = await service.get_restaurant_by_id(id)

# ❌ Bad - sync test for async code
def test_get_restaurant(self):
    result = service.get_restaurant_by_id(id)  # Won't work!
```

### 5. Use Type Hints

```python
# ✅ Good
async def test_example(
    self,
    test_session: AsyncSession,
    create_test_restaurant: Callable
):
    """Test with clear parameter types."""

# ❌ Bad
async def test_example(self, test_session, create_test_restaurant):
    """Test without type information."""
```

### 6. Test Edge Cases

For each feature, test:
- **Happy path**: Normal operation
- **Not found**: Missing resources
- **Invalid input**: Malformed data
- **Boundary conditions**: Empty, maximum, minimum values
- **Special characters**: Accents, spaces, unicode

```python
class TestListRestaurantsByCity:
    def test_list_by_city_with_results(self):        # Happy path
    def test_list_by_city_empty(self):               # Not found
    def test_list_by_city_case_sensitive(self):      # Edge case
    def test_list_by_city_with_spaces(self):         # Special chars
    def test_list_by_city_with_accents(self):        # Special chars
    def test_list_by_city_with_pagination(self):     # Boundary
```

### 7. Clean Test Data

```python
# ✅ Good - minimal realistic data
restaurant_data = RestaurantData(
    name="Test Restaurant",
    address="Calle 1",
    city="Tunja",
    phone="+57 300 123 4567",
)

# ❌ Bad - excessive irrelevant data
restaurant_data = RestaurantData(
    name="The Most Amazing Restaurant With A Very Long Name...",
    description="Lorem ipsum dolor sit amet, consectetur...",
    # 20 more fields...
)
```

### 8. Avoid Test Code Duplication

Use fixtures for repeated setup:

```python
# ✅ Good - reusable fixture
@pytest.fixture
def restaurant_data():
    return RestaurantData(
        name="Test Restaurant",
        city="Tunja",
        # common defaults
    )

def test_a(self, restaurant_data):
    # uses fixture

def test_b(self, restaurant_data):
    # reuses fixture

# ❌ Bad - copy-paste setup
def test_a(self):
    data = RestaurantData(name="Test", city="Tunja")
    
def test_b(self):
    data = RestaurantData(name="Test", city="Tunja")
```

---

## Examples

### Complete E2E Test

```python
"""E2E tests for GET /restaurants endpoint."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestListRestaurants:
    """E2E tests for listing restaurants."""

    def test_list_with_pagination(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test listing restaurants with pagination parameters.
        
        Given: 10 restaurants exist in database
        When: Requesting /restaurants?page=2&page_size=3
        Then: Returns 3 restaurants from page 2 with pagination metadata
        """
        # Arrange
        for i in range(10):
            await create_test_restaurant(name=f"Restaurant {i:02d}")

        # Act
        response = test_client.get("/restaurants?page=2&page_size=3")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 3
        assert data["pagination"]["total"] == 10

    def test_list_filter_by_city(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test filtering restaurants by city.
        
        Given: Restaurants exist in multiple cities
        When: Requesting /restaurants?city=Tunja
        Then: Returns only restaurants from Tunja
        """
        # Arrange
        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        response = test_client.get("/restaurants?city=Tunja")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 2
        assert all(r["city"] == "Tunja" for r in data["data"])
```

### Complete Integration Test

```python
"""Integration tests for RestaurantService."""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.services import RestaurantService
from app.domains.restaurants.repositories import RestaurantRepositorySQLite
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.shared.repositories.archive import ArchiveRepositorySQLite


class TestRestaurantServiceGet:
    """Integration tests for RestaurantService get operations."""

    @pytest.mark.asyncio
    async def test_get_restaurant_by_id_existing(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test getting an existing restaurant through service.
        
        Given: A restaurant exists in database
        When: Calling service.get_restaurant_by_id()
        Then: Returns restaurant entity
        """
        # Arrange
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)
        created = await create_test_restaurant(name="Test Restaurant")

        # Act
        result = await service.get_restaurant_by_id(created.id)

        # Assert
        assert result.id == created.id
        assert result.name == "Test Restaurant"

    @pytest.mark.asyncio
    async def test_get_restaurant_by_id_not_found(self, test_session: AsyncSession):
        """Test getting non-existent restaurant raises exception.
        
        Given: Restaurant ID that doesn't exist
        When: Calling service.get_restaurant_by_id()
        Then: Raises RestaurantNotFoundException
        """
        # Arrange
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act & Assert
        with pytest.raises(RestaurantNotFoundException):
            await service.get_restaurant_by_id(nonexistent_id)
```

### Complete Unit Test

```python
"""Unit tests for Restaurant entity."""

import pytest
from datetime import datetime, UTC
from pydantic import ValidationError, HttpUrl

from app.domains.restaurants.domain.entities import Restaurant, RestaurantData
from app.shared.domain import GeoLocation


class TestRestaurantData:
    """Unit tests for RestaurantData validation."""

    def test_create_restaurant_data_with_valid_minimal_data(self):
        """Test creating restaurant data with valid minimal required fields.
        
        Given: Valid minimal restaurant data
        When: Creating RestaurantData instance
        Then: Instance is created successfully with default values
        """
        # Arrange & Act
        restaurant_data = RestaurantData(
            name="Minimal Restaurant",
            address="Calle 1",
            city="Tunja",
            phone="+57 300 123 4567",
        )

        # Assert
        assert restaurant_data.name == "Minimal Restaurant"
        assert restaurant_data.state == "Boyacá"  # Default value
        assert restaurant_data.cuisine_types == []  # Default value

    def test_create_restaurant_data_with_invalid_name_empty(self):
        """Test creating restaurant data with empty name fails validation.
        
        Given: Restaurant data with empty name
        When: Creating RestaurantData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RestaurantData(
                name="",  # Invalid: empty name
                address="Calle 1",
                city="Tunja",
                phone="+57 300 123 4567",
            )

        # Assert
        assert "name" in str(exc_info.value)


class TestRestaurant:
    """Unit tests for Restaurant entity."""

    def test_restaurant_model_dump_mode_json_converts_http_url(self):
        """Test that HttpUrl fields convert to strings in JSON mode.
        
        Given: Restaurant entity with HttpUrl website
        When: Calling model_dump(mode="json")
        Then: Website is serialized as string
        """
        # Arrange
        restaurant = Restaurant(
            id="01HQZX123456789ABCDEFGHIJK",
            name="Test Restaurant",
            address="Calle 1",
            city="Tunja",
            state="Boyacá",
            country="Colombia",
            phone="+57 300 123 4567",
            website=HttpUrl("https://restaurant.com"),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        # Act
        dumped = restaurant.model_dump(mode="json")

        # Assert
        assert isinstance(dumped["website"], str)
        assert dumped["website"] == "https://restaurant.com/"
```

---

## Quick Reference

### Test Checklist

When writing a new test, ensure:

- [ ] File name matches source file: `test_{source_name}.py`
- [ ] Test class describes the component/feature
- [ ] Test function name describes scenario: `test_{action}_{scenario}`
- [ ] Docstring includes Given-When-Then
- [ ] Code includes AAA comments (Arrange-Act-Assert)
- [ ] Uses appropriate fixtures from conftest
- [ ] Async tests have `@pytest.mark.asyncio` decorator
- [ ] Type hints on all parameters
- [ ] Assertions are specific and descriptive
- [ ] Test is independent (doesn't rely on other tests)

### Running Tests

```bash
# All tests
uv run pytest

# Specific level
uv run pytest tests/domains/restaurants/e2e/
uv run pytest tests/domains/restaurants/integration/
uv run pytest tests/domains/restaurants/unit/

# Specific file
uv run pytest tests/domains/restaurants/e2e/public/test_get.py

# Specific test
uv run pytest tests/domains/restaurants/e2e/public/test_get.py::TestGetRestaurant::test_get_existing_restaurant

# With verbose output
uv run pytest -v

# With coverage
uv run pytest --cov=app
```

---

## Summary

This testing architecture provides:

1. **Clear Structure**: Tests mirror application organization
2. **Multiple Levels**: E2E, Integration, and Unit coverage
3. **Consistent Patterns**: Given-When-Then + AAA
4. **Fast Execution**: Entire suite runs in < 2 seconds
5. **Maintainability**: Easy to locate and update tests
6. **Documentation**: Tests serve as living documentation
7. **One File = One Class**: Each file contains exactly one test class (or closely related classes)
8. **Focused Files**: Average ~70-80 lines per file, easy to navigate
9. **Operation-Based Organization**: Integration tests split by method/operation

### Current Test Statistics

```
E2E Tests:         7 tests  (admin endpoints)
Integration Tests: 28 tests (8 files: 3 services + 5 repositories)
Unit Tests:        9 tests  (entities and value objects)
──────────────────────────────────────────────────────
TOTAL:            44 tests

Average file size: ~70-100 lines
Execution time:    < 2 seconds
```

Follow these guidelines to ensure consistent, high-quality test coverage across the entire application.

