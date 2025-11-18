# Restaurants Domain

## Overview

The **Restaurants Domain** is the core bounded context for managing restaurants, dishes, and ownership relationships in the Descubre Boyacá platform. This domain follows **Clean Architecture** principles with **Domain-Driven Design (DDD)** patterns, providing a comprehensive solution for restaurant discovery and management.

## Table of Contents

1. [Domain Responsibilities](#domain-responsibilities)
2. [Architecture Overview](#architecture-overview)
3. [Core Entities](#core-entities)
4. [Business Rules](#business-rules)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Usage Examples](#usage-examples)
8. [Testing](#testing)

---

## Domain Responsibilities

This domain handles:

- ✅ **Restaurant Management**: CRUD operations for restaurants
- ✅ **Dish Management**: Menu items with detailed nutritional and flavor profiles
- ✅ **Ownership Management**: Multi-owner support with roles and primary ownership
- ✅ **Search & Discovery**: Filter by city, cuisine, price level, features
- ✅ **Favorites Integration**: Works with the favorites domain
- ✅ **Audit Trail**: Complete archival system for deleted records
- ✅ **Authorization**: Role-based access (Admin, Owner, Public)

---

## Architecture Overview

The domain follows a **4-layer Clean Architecture**:

```
app/domains/restaurants/
├── domain/              # Layer 1: Enterprise Business Rules
│   ├── entities/        # Restaurant, Dish, RestaurantOwner
│   ├── enums/          # CuisineType, PriceLevel, RestaurantFeature, etc.
│   ├── exceptions/     # Domain-specific exceptions
│   └── interfaces/     # Repository contracts (Protocol-based)
│
├── application/         # Layer 2: Application Business Rules
│   └── services/       # RestaurantService, DishService, RestaurantOwnerService
│
├── infrastructure/      # Layer 3: Interface Adapters
│   ├── persistence/
│   │   ├── models/     # SQLModel ORM models
│   │   └── repositories/
│   │       ├── restaurant/
│   │       │   ├── postgresql.py
│   │       │   └── sqlite.py
│   │       ├── dish/
│   │       │   ├── postgresql.py
│   │       │   └── sqlite.py
│   │       └── restaurant_owner/
│   │           ├── postgresql.py
│   │           └── sqlite.py
│   └── dependencies/   # Dependency injection factories
│
└── presentation/        # Layer 4: Frameworks & Drivers
    └── api/
        ├── routes/     # FastAPI endpoints (Admin, Owner, Public)
        │   ├── restaurant/
        │   │   ├── admin/    # Admin-only operations
        │   │   ├── owner/    # Owner-specific operations
        │   │   └── public/   # Public access
        │   └── dish/
        │       ├── admin/
        │       ├── owner/
        │       └── public/
        └── schemas/    # Pydantic request/response models
```

### Key Architectural Decisions

1. **Services Pattern**: Currently uses services instead of use cases (legacy pattern)
2. **Multi-Database Support**: Separate PostgreSQL and SQLite repositories
3. **Composite Keys**: RestaurantOwner uses (restaurant_id, owner_id) composite primary key
4. **Audit Integration**: Mandatory archiving before deletion using Unit of Work pattern
5. **Role-Based Routes**: Separate route modules for admin, owner, and public access

---

## Core Entities

### 1. Restaurant

**Purpose**: Represents a restaurant establishment in Boyacá.

**Key Attributes**:
- **Identity**: `id` (ULID), audit fields (created_at, updated_at, created_by, updated_by)
- **Basic Info**: name, description, phone, email, website
- **Location**: address, city, state, postal_code, country, geolocation (GeoLocation)
- **Social**: social_media (SocialMedia value object)
- **Classification**: 
  - `establishment_types` (restaurant, cafe, bakery, bar, food_truck)
  - `cuisine_types` (colombiana, boyacense, internacional, etc.)
  - `price_level` (1-4: budget to luxury)
  - `features` (wifi, parking, pet_friendly, etc.)
  - `tags` (romantic, family_friendly, instagram_worthy, etc.)

**Domain Model**:
```python
class RestaurantData(BaseModel):
    """Restaurant data without system metadata."""
    name: str
    description: str | None
    address: str
    city: str
    state: str = "Boyacá"
    country: str = "Colombia"
    phone: str
    email: str | None
    website: HttpUrl | None
    location: GeoLocation | None
    social_media: SocialMedia | None
    establishment_types: list[str]
    cuisine_types: list[str]
    price_level: int | None  # 1-4
    features: list[str]
    tags: list[str]

class Restaurant(RestaurantData, Audit):
    """Complete entity with ID and audit trail."""
    # Inherits: id, created_at, updated_at, created_by, updated_by
```

### 2. Dish

**Purpose**: Represents a menu item belonging to a restaurant.

**Key Attributes**:
- **Identity**: `id` (ULID), `restaurant_id` (foreign key)
- **Basic Info**: name, description, category, image_url
- **Pricing**: price, original_price (for discounts)
- **Availability**: is_available, preparation_time_minutes, serves
- **Nutrition**: calories, dietary_restrictions, allergens, ingredients
- **Flavor**: flavor_profile (JSON: spicy, sweet, salty levels)
- **Display**: is_featured, display_order

**Domain Model**:
```python
class DishData(BaseModel):
    """Dish data without system metadata."""
    restaurant_id: str
    name: str
    description: str | None
    category: str  # appetizer, main_course, dessert, beverage
    price: Decimal
    original_price: Decimal | None
    is_available: bool = True
    preparation_time_minutes: int | None
    serves: int | None
    calories: int | None
    image_url: HttpUrl | None
    dietary_restrictions: list[str]
    ingredients: list[str]
    allergens: list[str]
    flavor_profile: dict[str, str]
    is_featured: bool = False
    display_order: int = 0

class Dish(DishData, Audit):
    """Complete entity with ID and audit trail."""
```

### 3. RestaurantOwner

**Purpose**: Represents the ownership/management relationship between users and restaurants.

**Key Attributes**:
- **Composite Key**: (restaurant_id, owner_id)
- **Role**: owner, manager, staff
- **Primary Ownership**: is_primary (only one per restaurant)
- **Audit**: created_at, updated_at, created_by, updated_by

**Domain Model**:
```python
class RestaurantOwnerData(BaseModel):
    """Ownership data without system metadata."""
    restaurant_id: str  # ULID (26 chars)
    owner_id: str       # ULID (26 chars)
    role: str = "owner"
    is_primary: bool = False

class RestaurantOwner(RestaurantOwnerData, Timestamp, UserTracking):
    """Complete ownership relationship with audit trail."""
    # No separate id field - uses composite PK (restaurant_id, owner_id)
```

---

## Business Rules

### Restaurant Rules

1. **Unique Constraint**: Restaurant names should be unique per city (not enforced at DB level)
2. **Location**: Geolocation is optional and can be added via geocoding
3. **Price Level**: Must be between 1-4 if provided
4. **State Default**: Defaults to "Boyacá" (department)
5. **Country Default**: Defaults to "Colombia"

### Dish Rules

1. **Restaurant Validation**: Restaurant must exist before creating a dish
2. **Price Constraints**: Price >= 0, max 10 digits with 2 decimal places
3. **Category Required**: Every dish must have a category
4. **Availability Toggle**: Can be enabled/disabled without deletion
5. **Display Order**: Lower numbers appear first in menus

### Ownership Rules

1. **Primary Owner**: Every restaurant should have exactly one primary owner
2. **No Duplicate Ownership**: (restaurant_id, owner_id) must be unique
3. **Cannot Remove Last Primary Owner**: Prevents orphaned restaurants
4. **Role Validation**: Only "owner", "manager", "staff" are valid roles
5. **Ownership Transfer**: New primary owner must already be an owner

---

## API Endpoints

### Restaurant Endpoints

#### Admin Endpoints (`/restaurants/admin`)

```http
POST   /restaurants/admin/                      # Create restaurant
DELETE /restaurants/admin/{id}                  # Delete restaurant (with archiving)
POST   /restaurants/admin/{id}/owners           # Assign owner
DELETE /restaurants/admin/{id}/owners/{owner_id} # Remove owner
PATCH  /restaurants/admin/{id}/owners/{owner_id} # Update owner role
POST   /restaurants/admin/{id}/transfer         # Transfer primary ownership
GET    /restaurants/admin/{id}/owners           # List restaurant owners
```

#### Owner Endpoints (`/restaurants/owner`)

```http
GET   /restaurants/owner/restaurants                      # List my restaurants
GET   /restaurants/owner/restaurants/{id}                 # Get my restaurant
PATCH /restaurants/owner/restaurants/{id}                 # Update my restaurant
GET   /restaurants/owner/restaurants/{id}/team           # List my team members
```

#### Public Endpoints (`/restaurants`)

```http
GET   /restaurants                   # List all restaurants (paginated, filtered)
GET   /restaurants/city/{city}       # List restaurants by city
GET   /restaurants/{id}              # Get restaurant by ID
GET   /restaurants/favorites         # List user's favorite restaurants
```

### Dish Endpoints

#### Admin Endpoints (`/restaurants/admin`)

```http
POST   /restaurants/admin/restaurants/{restaurant_id}/dishes  # Create dish
PATCH  /restaurants/admin/dishes/{dish_id}                    # Update dish
DELETE /restaurants/admin/dishes/{dish_id}                    # Delete dish
```

#### Owner Endpoints (`/restaurants/owner`)

```http
POST   /restaurants/owner/restaurants/{restaurant_id}/dishes  # Create dish
PATCH  /restaurants/owner/dishes/{dish_id}                    # Update dish
DELETE /restaurants/owner/dishes/{dish_id}                    # Delete dish
```

#### Public Endpoints (`/restaurants`)

```http
GET   /restaurants/{restaurant_id}/dishes     # List restaurant dishes
GET   /restaurants/dishes/{dish_id}           # Get dish by ID
```

---

## Database Schema

### Restaurants Table

```sql
CREATE TABLE restaurants (
    id VARCHAR(26) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    address VARCHAR(500) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) DEFAULT 'Boyacá',
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'Colombia',
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    website TEXT,
    location JSON,  -- {latitude, longitude}
    social_media JSON,  -- {facebook, instagram, twitter, etc.}
    establishment_types JSON,  -- ["restaurant", "cafe"]
    cuisine_types JSON,  -- ["colombiana", "boyacense"]
    price_level INTEGER CHECK (price_level >= 1 AND price_level <= 4),
    features JSON,  -- ["wifi", "parking"]
    tags JSON,  -- ["romantic", "family_friendly"]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(26),
    updated_by VARCHAR(26)
);
```

### Dishes Table

```sql
CREATE TABLE dishes (
    id VARCHAR(26) PRIMARY KEY,
    restaurant_id VARCHAR(26) NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    original_price DECIMAL(10, 2) CHECK (original_price >= 0),
    is_available BOOLEAN DEFAULT TRUE,
    preparation_time_minutes INTEGER CHECK (preparation_time_minutes >= 0),
    serves INTEGER CHECK (serves >= 1),
    calories INTEGER CHECK (calories >= 0),
    image_url TEXT,
    dietary_restrictions JSON,  -- ["vegetarian", "gluten_free"]
    ingredients JSON,  -- ["chicken", "rice", "vegetables"]
    allergens JSON,  -- ["nuts", "dairy"]
    flavor_profile JSON,  -- {"spicy": "hot", "savory": "high"}
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(26),
    updated_by VARCHAR(26),
    INDEX idx_restaurant_id (restaurant_id),
    INDEX idx_category (category),
    INDEX idx_is_available (is_available)
);
```

### Restaurant Owners Table

```sql
CREATE TABLE restaurant_owners (
    restaurant_id VARCHAR(26) NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    owner_id VARCHAR(26) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'owner',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(26),
    updated_by VARCHAR(26),
    PRIMARY KEY (restaurant_id, owner_id),
    INDEX idx_owner_id (owner_id),
    INDEX idx_is_primary (is_primary)
);
```

---

## Usage Examples

### Creating a Restaurant

```python
from app.domains.restaurants import RestaurantService, RestaurantData

# Create restaurant data
restaurant_data = RestaurantData(
    name="La Casona Boyacense",
    description="Traditional Boyacá cuisine in the heart of Tunja",
    address="Calle 19 # 9-45",
    city="Tunja",
    state="Boyacá",
    country="Colombia",
    phone="+57 320 123 4567",
    email="contacto@lacasonaboyacense.com",
    website="https://lacasonaboyacense.com",
    establishment_types=["restaurant", "cafe"],
    cuisine_types=["boyacense", "colombiana"],
    price_level=2,  # Moderate
    features=["wifi", "parking", "outdoor_seating"],
    tags=["traditional", "family_friendly"]
)

# Create restaurant
restaurant = await restaurant_service.create_restaurant(
    restaurant_data,
    created_by="01BX5ZZKBKACTAV9WEVGEMMVS0"
)
```

### Adding a Dish

```python
from app.domains.restaurants import DishService, DishData
from decimal import Decimal

dish_data = DishData(
    restaurant_id=restaurant.id,
    name="Cuchuco de Trigo",
    description="Traditional wheat soup with pork ribs and vegetables",
    category="main_course",
    price=Decimal("25000"),
    is_available=True,
    preparation_time_minutes=30,
    serves=1,
    calories=450,
    dietary_restrictions=["dairy"],
    ingredients=["wheat", "pork_ribs", "potatoes", "fava_beans"],
    allergens=["gluten"],
    flavor_profile={"hearty": "high", "savory": "high", "spicy": "low"},
    is_featured=True,
    display_order=1
)

dish = await dish_service.create_dish(
    dish_data,
    restaurant_id=restaurant.id,
    created_by=owner_id
)
```

### Assigning Restaurant Owner

```python
from app.domains.restaurants import RestaurantOwnerService

# Assign primary owner
ownership = await owner_service.assign_owner(
    restaurant_id=restaurant.id,
    owner_id="01BX5ZZKBKACTAV9WEVGEMMVS0",
    role="owner",
    is_primary=True,
    assigned_by=admin_id
)

# Add a manager
manager = await owner_service.assign_owner(
    restaurant_id=restaurant.id,
    owner_id="01BX5ZZKBKACTAV9WEVGEMMVS1",
    role="manager",
    is_primary=False,
    assigned_by=admin_id
)
```

### Searching Restaurants

```python
# List all restaurants in Tunja
restaurants, total = await restaurant_service.list_restaurants_by_city(
    city="Tunja",
    offset=0,
    limit=20
)

# Filter by price level and features
filters = {
    "city": "Tunja",
    "price_level": 2,
    "features": ["wifi", "parking"]
}
restaurants, total = await restaurant_service.find_restaurants(
    filters=filters,
    offset=0,
    limit=20
)
```

### Deleting with Archive

```python
# Delete restaurant (archives automatically using Unit of Work)
await restaurant_service.delete_restaurant(
    restaurant_id=restaurant.id,
    deleted_by=admin_id,
    note="Restaurant permanently closed"
)
# Both archive and delete happen atomically
```

---

## Testing

### Test Structure

```
tests/domains/restaurants/
├── unit/
│   ├── test_restaurant_entity.py
│   ├── test_dish_entity.py
│   ├── test_restaurant_owner_entity.py
│   └── test_services.py
│
├── integration/
│   ├── test_restaurant_repository.py
│   ├── test_dish_repository.py
│   ├── test_restaurant_owner_repository.py
│   ├── test_restaurant_service.py
│   ├── test_dish_service.py
│   └── test_ownership_service.py
│
└── e2e/
    ├── test_restaurant_crud.py
    ├── test_dish_crud.py
    ├── test_ownership_management.py
    ├── test_restaurant_search.py
    ├── test_authorization.py
    └── test_favorites_integration.py
```

### Running Tests

```bash
# Run all restaurant tests
pytest tests/domains/restaurants/

# Run only unit tests
pytest tests/domains/restaurants/unit/

# Run only integration tests
pytest tests/domains/restaurants/integration/

# Run only e2e tests
pytest tests/domains/restaurants/e2e/

# Run with coverage
pytest tests/domains/restaurants/ --cov=app/domains/restaurants --cov-report=html
```

---

## Domain Enums

### CuisineType
Colombian: `boyacense`, `colombiana`, `santandereana`, `antioqueña`, `costeña`
International: `italiana`, `mexicana`, `china`, `japonesa`, `peruana`, `argentina`
Special: `fusion`, `vegetariana`, `vegana`, `parrilla`, `mariscos`

### PriceLevel
- `1` (BUDGET): < $20,000 COP
- `2` (MODERATE): $20,000 - $40,000 COP
- `3` (EXPENSIVE): $40,000 - $80,000 COP
- `4` (LUXURY): > $80,000 COP

### RestaurantFeature
Connectivity: `wifi`, `tv`
Seating: `parking`, `outdoor_seating`, `private_rooms`, `terrace`
Services: `delivery`, `takeout`, `reservations`, `online_order`
Family: `kids_menu`, `pet_friendly`, `family_friendly`
Dietary: `vegetarian_options`, `vegan_options`, `gluten_free_options`
Entertainment: `live_music`, `sports_on_tv`, `karaoke`

### EstablishmentType
`restaurant`, `cafe`, `bakery`, `bar`, `food_truck`, `buffet`, `fine_dining`

### DishCategory
`appetizer`, `main_course`, `side_dish`, `dessert`, `beverage`, `soup`, `salad`

### DietaryRestriction
`vegetarian`, `vegan`, `gluten_free`, `lactose_free`, `nut_free`, `dairy_free`

### OwnerRole
`owner`, `manager`, `staff`

---

## Domain Exceptions

| Exception | Scenario | HTTP Status |
|-----------|----------|-------------|
| `RestaurantNotFoundException` | Restaurant ID not found | 404 |
| `RestaurantAlreadyExistsException` | Duplicate restaurant | 409 |
| `DishNotFoundException` | Dish ID not found | 404 |
| `OwnershipNotFoundException` | Ownership relationship not found | 404 |
| `OwnershipAlreadyExistsException` | Duplicate ownership | 409 |
| `CannotRemovePrimaryOwnerException` | Trying to remove last owner | 400 |
| `InvalidOwnerRoleException` | Invalid role value | 400 |
| `OwnerNotAssignedException` | Owner not assigned to restaurant | 403 |
| `InvalidCuisineTypeException` | Invalid cuisine type | 400 |
| `InvalidPriceLevelException` | Price level not 1-4 | 400 |

---

## Dependencies

### Internal Dependencies
- `app.domains.audit` - Archive system for deleted records
- `app.domains.favorites` - Favorite restaurants integration
- `app.domains.users` - User references for ownership
- `app.domains.auth` - Authentication and authorization
- `app.shared` - Common entities, value objects, patterns

### External Dependencies
- `fastapi` - REST API framework
- `pydantic` - Data validation and serialization
- `sqlmodel` - ORM for database models
- `ulid` - Unique identifiers
- `python-ulid` - ULID generation

---

## Future Enhancements (See TODO.md)

- [ ] Migrate from Services to Use Cases pattern
- [ ] Add restaurant hours/schedule management
- [ ] Implement dish variations (sizes, extras)
- [ ] Add restaurant images/gallery
- [ ] Implement menu sections/categories
- [ ] Add seasonal menu support
- [ ] Implement reservation system integration
- [ ] Add restaurant statistics and analytics

---

## Contributing

When extending this domain:

1. **Follow Clean Architecture**: Keep layers separated
2. **Use Type Hints**: All functions must have type annotations
3. **Write Docstrings**: Google-style docstrings required
4. **Test Coverage**: Unit + Integration + E2E tests
5. **Domain Exceptions**: Create specific exceptions for business rules
6. **Repository Pattern**: Implement both PostgreSQL and SQLite repositories
7. **Consider Use Cases**: Prefer use cases over expanding services

---

## Related Documentation

- [Architecture Documentation](../../../ARCHITECTURE.md)
- [Audit System Proposal](../../../project/AUDIT_SYSTEM_PROPOSAL.md)
- [API Documentation](http://localhost:8000/docs) (when server is running)
- [Testing Guide](../../../tests/README.md)

---

**Last Updated**: November 2024  
**Maintainer**: Descubre Boyacá Team  
**Status**: ✅ Complete and Production-Ready

