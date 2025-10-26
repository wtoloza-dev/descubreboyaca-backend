# Test Fixtures

This directory contains all test fixtures organized by responsibility and domain. Fixtures are reusable test components that provide common setup, mock data, and dependencies for tests.

## 📁 Structure

```
fixtures/
├── README.md                           # This file
├── database.py                         # Database engine and session fixtures
├── clients.py                          # HTTP test clients with various auth levels
├── auth_users.py                       # Mock user entities for auth testing
└── domains/                            # Domain-specific fixtures
    ├── auth.py                         # Auth domain fixtures
    ├── restaurants.py                  # Restaurant domain factories & sample data
    ├── restaurant_services.py          # Restaurant domain service fixtures
    └── restaurant_repositories.py      # Restaurant domain repository fixtures
```

## 🎯 What are Fixtures?

Fixtures in pytest are functions that provide reusable setup code for tests. They:
- **Provide dependencies**: Database sessions, services, repositories
- **Create test data**: Sample entities, mock users
- **Configure test clients**: HTTP clients with different auth levels
- **Ensure isolation**: Each test gets a clean state

### Example

```python
@pytest.fixture(name="test_session")
async def fixture_test_session(test_engine):
    """Create a test database session.
    
    This fixture provides a clean async database session for each test.
    """
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session
```

Usage in tests:

```python
async def test_create_restaurant(test_session):
    restaurant = RestaurantModel(name="Test")
    test_session.add(restaurant)
    await test_session.commit()
    assert restaurant.id is not None
```

## 📚 Categories

### 1. Database Fixtures (`database.py`)

Core fixtures for database access.

| Fixture | Description | Scope | Usage |
|---------|-------------|-------|-------|
| `test_engine` | SQLite async engine | function | Rarely used directly |
| `test_session` | Async DB session | function | `async def test_xxx(test_session)` |

**Example:**
```python
async def test_create_user(test_session):
    user = UserModel(email="test@example.com")
    test_session.add(user)
    await test_session.commit()
```

### 2. Client Fixtures (`clients.py`)

HTTP test clients with different authentication levels for E2E testing.

| Fixture | Auth Level | Mock User | Usage |
|---------|------------|-----------|-------|
| `test_client` | None (public) | - | Public endpoints |
| `admin_client` | ADMIN | `mock_admin_user` | Admin endpoints |
| `owner_client` | OWNER | `mock_owner_user` | Owner endpoints |
| `user_client` | USER | `mock_regular_user` | User endpoints |

**Example:**
```python
def test_list_restaurants(test_client):
    response = test_client.get("/api/v1/restaurants")
    assert response.status_code == 200

def test_delete_restaurant(admin_client):
    response = admin_client.delete("/api/v1/admin/restaurants/123")
    assert response.status_code == 204
```

**Key Feature**: Clients automatically override auth dependencies, so you don't need to handle JWT tokens in tests.

### 3. Mock User Fixtures (`auth_users.py`)

Mock user entities for authentication testing.

| Fixture | Role | Email | Description |
|---------|------|-------|-------------|
| `mock_admin_user` | ADMIN | admin@test.com | Admin user entity |
| `mock_owner_user` | OWNER | owner@test.com | Owner user entity |
| `mock_regular_user` | USER | user@test.com | Regular user entity |

**Example:**
```python
def test_admin_access(mock_admin_user):
    assert mock_admin_user.role == UserRole.ADMIN
    assert mock_admin_user.email == "admin@test.com"
```

### 4. Auth Domain Fixtures (`domains/auth.py`)

Authentication-specific fixtures for users, passwords, tokens, and services.

| Fixture | Type | Description |
|---------|------|-------------|
| `test_password` | Data | Password with bcrypt hash |
| `create_test_user` | Factory | Create users in DB |
| `password_service` | Service | BcryptPasswordHasher |
| `token_provider` | Service | JWTTokenProvider |
| `auth_service` | Service | Complete auth service |
| `user_repository` | Repository | User data access |

**Example:**
```python
async def test_login(auth_service, create_test_user, test_password):
    user = await create_test_user(
        email="test@example.com",
        hashed_password=test_password.hashed_password
    )
    tokens = await auth_service.login(
        email="test@example.com",
        password=test_password.password
    )
    assert tokens.access_token is not None
```

### 5. Restaurant Domain Fixtures

#### Sample Data (`domains/restaurants.py`)

Pre-configured sample data for quick testing.

| Fixture | Type | Description |
|---------|------|-------------|
| `sample_restaurant_data` | RestaurantData | "La Casona Boyacense" in Tunja |
| `sample_dish_data` | DishData | "Ajiaco Santafereño" |

**Example:**
```python
async def test_create_with_sample(restaurant_service, sample_restaurant_data):
    restaurant = await restaurant_service.create(sample_restaurant_data)
    assert restaurant.name == "La Casona Boyacense"
```

#### Factory Fixtures (`domains/restaurants.py`)

Factory fixtures return callable functions to create multiple test entities.

| Fixture | Returns | Description |
|---------|---------|-------------|
| `create_test_restaurant` | async callable | Create restaurants in DB |
| `create_test_ownership` | async callable | Create ownership relations |
| `create_test_dish` | async callable | Create dishes in DB |

**Example:**
```python
async def test_list_dishes(create_test_restaurant, create_test_dish):
    restaurant = await create_test_restaurant(name="Test Restaurant")
    
    # Create multiple dishes
    dish1 = await create_test_dish(restaurant_id=restaurant.id, name="Dish 1")
    dish2 = await create_test_dish(restaurant_id=restaurant.id, name="Dish 2")
    dish3 = await create_test_dish(restaurant_id=restaurant.id, name="Dish 3")
    
    # Test listing logic
    dishes = await service.list_dishes(restaurant.id)
    assert len(dishes) == 3
```

#### Service Fixtures (`domains/restaurant_services.py`)

Fully configured service instances for integration testing.

| Fixture | Service | Dependencies |
|---------|---------|--------------|
| `restaurant_service` | RestaurantService | Repository + Archive service |
| `dish_service` | DishService | Repositories + Archive service |
| `owner_service` | RestaurantOwnerService | Repositories |

**Example:**
```python
async def test_create_dish(dish_service, create_test_restaurant):
    restaurant = await create_test_restaurant()
    data = DishData(name="Test Dish", price=Decimal("10.00"))
    
    dish = await dish_service.create_dish(data, restaurant.id, "user_123")
    assert dish.name == "Test Dish"
```

#### Repository Fixtures (`domains/restaurant_repositories.py`)

Repository instances for data access testing.

| Fixture | Repository | Description |
|---------|------------|-------------|
| `restaurant_repository` | RestaurantRepositorySQLite | Restaurant data access |
| `dish_repository` | DishRepositorySQLite | Dish data access |
| `owner_repository` | RestaurantOwnerRepositorySQLite | Ownership data access |

**Example:**
```python
async def test_find_by_city(restaurant_repository, create_test_restaurant):
    await create_test_restaurant(name="Restaurant 1", city="Tunja")
    await create_test_restaurant(name="Restaurant 2", city="Tunja")
    
    restaurants = await restaurant_repository.find_by_city("Tunja")
    assert len(restaurants) == 2
```

## 🎨 Design Patterns

### 1. Factory Pattern

Factory fixtures return callable functions to create multiple instances:

```python
@pytest.fixture(name="create_test_restaurant")
def fixture_create_test_restaurant(test_session: AsyncSession):
    async def _create_restaurant(**kwargs) -> RestaurantModel:
        data = {
            "id": generate_ulid(),
            "name": "Test Restaurant",
            # ... defaults ...
        }
        data.update(kwargs)
        
        restaurant = RestaurantModel(**data)
        test_session.add(restaurant)
        await test_session.commit()
        return restaurant
    
    return _create_restaurant
```

**Why?** Allows creating multiple entities with different data in a single test.

### 2. Dependency Injection

Service and repository fixtures use dependency injection:

```python
@pytest.fixture(name="restaurant_service")
def fixture_restaurant_service(test_session: AsyncSession):
    repository = RestaurantRepositorySQLite(test_session)
    archive_service = ArchiveService(ArchiveRepositorySQLite(test_session))
    return RestaurantService(repository, archive_service)
```

**Why?** Tests the real service with real dependencies, not mocks (integration testing).

### 3. Override Pattern

Client fixtures override FastAPI dependencies:

```python
@pytest.fixture(name="admin_client")
def fixture_admin_client(test_session, mock_admin_user):
    from app.main import app
    
    async def get_test_session_override():
        yield test_session
    
    async def get_mock_admin():
        return mock_admin_user
    
    app.dependency_overrides[get_async_session_dependency] = get_test_session_override
    app.dependency_overrides[require_admin_dependency] = get_mock_admin
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()
```

**Why?** Bypasses auth for E2E tests, focusing on business logic, not authentication.

## 🧪 Testing Levels

### E2E Testing (Endpoint Level)

Use client fixtures to test complete HTTP flows:

```python
async def test_create_dish_e2e(
    owner_client,
    mock_owner_user,
    create_test_restaurant,
    create_test_ownership
):
    restaurant = await create_test_restaurant()
    await create_test_ownership(
        owner_id=mock_owner_user.id,
        restaurant_id=restaurant.id
    )
    
    response = owner_client.post(
        f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/dishes",
        json={"name": "New Dish", "price": 15.99}
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == "New Dish"
```

### Integration Testing (Service Level)

Use service fixtures to test business logic:

```python
async def test_create_dish_integration(
    dish_service,
    create_test_restaurant
):
    restaurant = await create_test_restaurant()
    data = DishData(name="Test Dish", price=Decimal("10.00"))
    
    dish = await dish_service.create_dish(data, restaurant.id, "user_123")
    
    assert dish.name == "Test Dish"
    assert dish.restaurant_id == restaurant.id
```

### Integration Testing (Repository Level)

Use repository fixtures to test data access:

```python
async def test_find_by_email_integration(
    user_repository,
    create_test_user
):
    user = await create_test_user(email="test@example.com")
    
    found = await user_repository.find_by_email("test@example.com")
    
    assert found is not None
    assert found.id == user.id
```

### Unit Testing (Domain Logic)

No fixtures needed for pure domain logic:

```python
def test_dish_validation():
    dish = Dish(name="Test", price=Decimal("10.00"))
    assert dish.price > 0
```

## ✅ Best Practices

### 1. Use the Right Level

```python
# ✅ Good: E2E test uses client
def test_delete_dish(admin_client):
    response = admin_client.delete("/api/v1/admin/dishes/123")
    assert response.status_code == 204

# ✅ Good: Integration test uses service
async def test_delete_dish(dish_service):
    await dish_service.delete_dish("123")
    # Assert in DB or repository

# ✅ Good: Unit test uses domain entities
def test_dish_price_validation():
    with pytest.raises(ValidationError):
        Dish(name="Test", price=Decimal("-10.00"))
```

### 2. Keep Fixtures Focused

```python
# ✅ Good: Single responsibility
@pytest.fixture(name="test_session")
async def fixture_test_session(test_engine):
    async with AsyncSession(test_engine) as session:
        yield session

# ❌ Bad: Does too much
@pytest.fixture(name="test_session_with_data")
async def fixture_test_session_with_data(test_engine):
    async with AsyncSession(test_engine) as session:
        # Don't create data in fixtures
        user = User(...)
        session.add(user)
        await session.commit()
        yield session
```

### 3. Use Factory Fixtures for Multiple Entities

```python
# ✅ Good: Factory pattern
async def test_pagination(create_test_restaurant):
    for i in range(10):
        await create_test_restaurant(name=f"Restaurant {i}")
    # Test pagination

# ❌ Bad: Creating fixtures for each entity
async def test_pagination(
    restaurant1, restaurant2, restaurant3, restaurant4, ...
):
    # Too many fixture parameters
```

### 4. Document Fixtures

Every fixture should have:
- Docstring explaining purpose
- Parameter descriptions
- Return type annotation
- Usage example

```python
@pytest.fixture(name="dish_service")
def fixture_dish_service(test_session: AsyncSession) -> DishService:
    """Create a dish service instance for testing.

    This fixture provides a fully configured DishService with
    all required dependencies injected.

    Args:
        test_session: Database session

    Returns:
        DishService: Configured dish service

    Example:
        >>> async def test_create_dish(dish_service):
        ...     dish = await dish_service.create_dish(data, "restaurant_id")
        ...     assert dish.name == "Test Dish"
    """
    # Implementation
```

### 5. Keep Test Data Realistic

```python
# ✅ Good: Realistic data
sample_restaurant_data = RestaurantData(
    name="La Casona Boyacense",
    city="Tunja",
    phone="+57 300 123 4567",
    cuisine_types=["Colombian", "Traditional"]
)

# ❌ Bad: Minimal/fake data
sample_restaurant_data = RestaurantData(
    name="Test",
    city="City",
    phone="123",
    cuisine_types=[]
)
```

## 🚀 Adding New Domain Fixtures

When adding a new domain (e.g., `bookings`):

### 1. Create Fixture Modules

```bash
touch tests/fixtures/domains/bookings.py
touch tests/fixtures/domains/booking_services.py
touch tests/fixtures/domains/booking_repositories.py
```

### 2. Define Fixtures

```python
# tests/fixtures/domains/bookings.py
import pytest

@pytest.fixture(name="sample_booking_data")
def fixture_sample_booking_data():
    return BookingData(...)

@pytest.fixture(name="create_test_booking")
def fixture_create_test_booking(test_session):
    async def _create(**kwargs):
        # Implementation
        pass
    return _create
```

### 3. Import in Domain Conftest

```python
# tests/domains/bookings/conftest.py
from tests.fixtures.domains.bookings import (
    fixture_create_test_booking,
    fixture_sample_booking_data,
)
from tests.fixtures.domains.booking_services import (
    fixture_booking_service,
)
```

### 4. Use in Tests

```python
# tests/domains/bookings/e2e/test_create.py
async def test_create_booking(user_client, create_test_booking):
    booking = await create_test_booking(...)
    response = user_client.get(f"/api/v1/bookings/{booking.id}")
    assert response.status_code == 200
```

## 🔍 Debugging Fixtures

### List All Available Fixtures

```bash
pytest --fixtures
```

### Show Fixture Setup/Teardown

```bash
pytest tests/path/to/test.py -v --setup-show
```

### Debug Specific Fixture

Add `import pdb; pdb.set_trace()` in the fixture:

```python
@pytest.fixture(name="test_session")
async def fixture_test_session(test_engine):
    async with AsyncSession(test_engine) as session:
        import pdb; pdb.set_trace()  # Debug here
        yield session
```

## 📊 Current Fixture Inventory

- **Total Fixtures**: 28
- **Database**: 2
- **Clients**: 4 (public, admin, owner, user)
- **Mock Users**: 3
- **Auth Domain**: 6
- **Restaurant Domain**: 12 (data, factories, services, repositories)
- **Helpers**: 1

## 📚 References

- [pytest fixtures documentation](https://docs.pytest.org/en/stable/fixture.html)
- [SQLModel testing guide](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Last Updated**: 2025-10-26  
**Fixtures Version**: 2.0 (Reorganized structure)

