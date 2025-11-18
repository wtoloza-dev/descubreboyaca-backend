# Restaurants Domain - TODO

This document tracks pending tasks, improvements, and future enhancements for the Restaurants domain.

## 🔴 Critical Issues

None at the moment. The domain is complete and functional.

---

## 🟡 Architectural Improvements

### 1. Migrate from Services to Use Cases Pattern

**Priority**: Medium  
**Effort**: Large  
**Status**: Planned

**Context**:  
According to the project's architecture guidelines (ARCHITECTURE.md), the preferred pattern is **Use Cases** over **Services**. The current implementation uses services which violates the Single Responsibility Principle and makes testing more complex.

**Current State**:
```
application/
└── services/
    ├── restaurant.py (12+ methods)
    ├── dish.py (8+ methods)
    └── restaurant_owner.py (10+ methods)
```

**Desired State**:
```
application/
├── services/ (only for complex domain logic)
└── use_cases/
    ├── restaurant/
    │   ├── create_restaurant.py
    │   ├── update_restaurant.py
    │   ├── delete_restaurant.py
    │   ├── find_restaurant_by_id.py
    │   ├── list_restaurants.py
    │   ├── list_restaurants_by_city.py
    │   └── list_user_favorite_restaurants.py
    ├── dish/
    │   ├── create_dish.py
    │   ├── update_dish.py
    │   ├── delete_dish.py
    │   ├── find_dish_by_id.py
    │   ├── list_restaurant_dishes.py
    │   └── toggle_dish_availability.py
    └── ownership/
        ├── assign_owner.py
        ├── remove_owner.py
        ├── update_owner_role.py
        ├── transfer_primary_ownership.py
        ├── list_restaurant_owners.py
        ├── list_user_restaurants.py
        └── verify_ownership.py
```

**Benefits**:
- ✅ Single responsibility per use case
- ✅ Easier to test individually
- ✅ Better for parallel development
- ✅ AI-friendly (clear prompt per operation)
- ✅ Follows project architecture guidelines

**Implementation Steps**:
1. [ ] Create `use_cases/` directory structure
2. [ ] Extract each service method into separate use case
3. [ ] Update dependency injection in `infrastructure/dependencies/`
4. [ ] Update routes to use use cases instead of services
5. [ ] Update tests to test use cases
6. [ ] Keep services only for complex domain calculations (if any)

**Example Migration**:
```python
# Before: app/domains/restaurants/application/services/restaurant.py
class RestaurantService:
    async def create_restaurant(self, data, created_by):
        return await self.repository.create(data, created_by=created_by)
    
    async def find_restaurant_by_id(self, restaurant_id):
        restaurant = await self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)
        return restaurant
    # ... 10 more methods

# After: app/domains/restaurants/application/use_cases/restaurant/create_restaurant.py
class CreateRestaurantUseCase:
    """Use case for creating a new restaurant."""
    
    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        self.repository = repository
    
    async def execute(
        self,
        restaurant_data: RestaurantData,
        created_by: str | None = None,
    ) -> Restaurant:
        """Execute the create restaurant use case."""
        return await self.repository.create(restaurant_data, created_by=created_by)

# After: app/domains/restaurants/application/use_cases/restaurant/find_restaurant_by_id.py
class FindRestaurantByIdUseCase:
    """Use case for finding a restaurant by ID."""
    
    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        self.repository = repository
    
    async def execute(self, restaurant_id: str) -> Restaurant:
        """Execute the find restaurant by ID use case."""
        restaurant = await self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)
        return restaurant
```

**References**:
- See `app/domains/audit/` for a complete use case implementation example
- ARCHITECTURE.md Section 4.3 "Use Cases Pattern"
- ARCHITECTURE.md Section 9.2 "Why Use Cases over Services?"

---

### 2. Optimize Favorites Query Performance

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Context**:  
The current implementation in `RestaurantService.list_user_favorites()` fetches restaurants one by one in a loop, which is inefficient.

**Current Implementation**:
```python
# app/domains/restaurants/application/services/restaurant.py:352
for restaurant_id in restaurant_ids:
    restaurant = await self.repository.get_by_id(restaurant_id)
    if restaurant:
        restaurants.append(restaurant)
```

**Proposed Solution**:
```python
# Add bulk query method to repository interface
async def get_by_ids(self, ids: list[str]) -> list[Restaurant]:
    """Get multiple restaurants by their IDs."""
    ...

# Update service method
restaurant_ids = [favorite.entity_id for favorite in favorites]
if not restaurant_ids:
    return [], 0

restaurants = await self.repository.get_by_ids(restaurant_ids)
return restaurants, total
```

**Benefits**:
- Single database query instead of N queries
- Significant performance improvement for users with many favorites

**Implementation**:
1. [ ] Add `get_by_ids()` method to `RestaurantRepositoryInterface`
2. [ ] Implement in PostgreSQL and SQLite repositories
3. [ ] Update `RestaurantService.list_user_favorites()` to use bulk query
4. [ ] Add tests for bulk query

---

## 🟢 Feature Enhancements

### 3. Restaurant Operating Hours

**Priority**: Medium  
**Effort**: Medium  
**Status**: Not Started

**Description**:  
Add support for restaurant operating hours with day-specific schedules, special hours, and holiday closures.

**Requirements**:
- [ ] Create `RestaurantHours` entity
  - Day of week (Monday-Sunday)
  - Opening time
  - Closing time
  - Is closed (for special days)
- [ ] Support multiple time ranges per day (e.g., lunch and dinner)
- [ ] Add "currently open" query filter
- [ ] Add special hours/exceptions (holidays)

**Schema**:
```python
class RestaurantHoursData(BaseModel):
    restaurant_id: str
    day_of_week: int  # 0=Monday, 6=Sunday
    opening_time: time
    closing_time: time
    is_closed: bool = False

class RestaurantHours(RestaurantHoursData, Audit):
    """Restaurant operating hours entity."""
```

**API Endpoints**:
```
POST   /restaurants/owner/restaurants/{id}/hours       # Add hours
PUT    /restaurants/owner/restaurants/{id}/hours       # Update hours
DELETE /restaurants/owner/restaurants/{id}/hours/{day} # Remove hours
GET    /restaurants/{id}/hours                         # Get hours
GET    /restaurants/open-now                           # Find open restaurants
```

---

### 4. Dish Variations (Sizes, Extras)

**Priority**: Medium  
**Effort**: Large  
**Status**: Not Started

**Description**:  
Add support for dish variations (sizes) and customizable extras/add-ons.

**Requirements**:
- [ ] Create `DishVariation` entity (Small, Medium, Large)
- [ ] Create `DishExtra` entity (extra cheese, bacon, etc.)
- [ ] Link variations and extras to dishes
- [ ] Update pricing logic to handle variations

**Schema**:
```python
class DishVariation(BaseModel):
    dish_id: str
    name: str  # "Small", "Medium", "Large"
    price_modifier: Decimal  # +/- amount from base price
    description: str | None
    is_available: bool = True

class DishExtra(BaseModel):
    dish_id: str
    name: str  # "Extra cheese", "Bacon"
    price: Decimal
    is_available: bool = True
```

---

### 5. Restaurant Image Gallery

**Priority**: Low  
**Effort**: Medium  
**Status**: Not Started

**Description**:  
Add support for multiple restaurant images (logo, cover, interior, exterior, food photos).

**Requirements**:
- [ ] Create `RestaurantImage` entity
- [ ] Support image types (logo, cover, gallery)
- [ ] Add primary image designation
- [ ] Add display order
- [ ] Integration with image storage service (S3, Cloudinary)

**Schema**:
```python
class RestaurantImage(BaseModel):
    restaurant_id: str
    image_url: HttpUrl
    image_type: str  # logo, cover, interior, exterior, food
    is_primary: bool = False
    display_order: int = 0
    caption: str | None
```

---

### 6. Menu Sections/Categories

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Add support for organizing dishes into menu sections (Appetizers, Main Courses, Desserts, etc.).

**Requirements**:
- [ ] Create `MenuSection` entity
- [ ] Link dishes to sections
- [ ] Support section ordering
- [ ] Support section availability (breakfast menu, lunch menu, etc.)

**Schema**:
```python
class MenuSection(BaseModel):
    restaurant_id: str
    name: str  # "Appetizers", "Main Courses"
    description: str | None
    display_order: int = 0
    is_available: bool = True
    availability_times: dict[str, str] | None  # {"start": "06:00", "end": "11:00"}
```

---

### 7. Seasonal Menu Support

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Add support for seasonal dishes and limited-time offers.

**Requirements**:
- [ ] Add `available_from` and `available_until` dates to `Dish`
- [ ] Add query filters for seasonal dishes
- [ ] Add "limited time" badge/flag

**Schema Changes**:
```python
class DishData(BaseModel):
    # ... existing fields ...
    available_from: date | None  # Start date for seasonal dish
    available_until: date | None  # End date for seasonal dish
    is_seasonal: bool = False
    is_limited_time: bool = False
```

---

### 8. Reservation System Integration

**Priority**: Low  
**Effort**: Large  
**Status**: Not Started

**Description**:  
Add support for table reservations (or integrate with external reservation system).

**Requirements**:
- [ ] Create `Reservation` entity (could be separate domain)
- [ ] Add table management
- [ ] Add time slot availability
- [ ] Add reservation confirmation/cancellation
- [ ] Email notifications

**Note**: This might warrant a separate `reservations` domain following DDD principles.

---

### 9. Restaurant Statistics & Analytics

**Priority**: Low  
**Effort**: Medium  
**Status**: Not Started

**Description**:  
Add analytics and statistics for restaurant owners.

**Requirements**:
- [ ] View count tracking
- [ ] Favorite count
- [ ] Review statistics (average rating, count)
- [ ] Popular dishes (most viewed, most ordered)
- [ ] Owner dashboard with metrics

**API Endpoints**:
```
GET /restaurants/owner/restaurants/{id}/statistics
GET /restaurants/owner/restaurants/{id}/analytics?period=month
```

---

## 🔵 Technical Debt

### 10. Add Composite Index for Restaurant Search

**Priority**: Medium  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Add composite indexes to improve query performance for common search patterns.

**Proposed Indexes**:
```sql
CREATE INDEX idx_restaurants_city_price_level ON restaurants(city, price_level);
CREATE INDEX idx_restaurants_city_cuisine ON restaurants(city, cuisine_types);
CREATE INDEX idx_dishes_restaurant_category ON dishes(restaurant_id, category);
CREATE INDEX idx_dishes_restaurant_available ON dishes(restaurant_id, is_available);
```

---

### 11. Add Input Validation for JSON Fields

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Add stricter validation for JSON array fields (cuisine_types, features, tags, etc.).

**Requirements**:
- [ ] Validate enum values (e.g., ensure cuisine_types only contains valid cuisines)
- [ ] Validate feature values against `RestaurantFeature` enum
- [ ] Add max length constraints for arrays
- [ ] Add custom Pydantic validators

**Example**:
```python
from pydantic import field_validator

class RestaurantData(BaseModel):
    cuisine_types: list[str] = Field(default_factory=list)
    
    @field_validator("cuisine_types")
    @classmethod
    def validate_cuisine_types(cls, v: list[str]) -> list[str]:
        valid_cuisines = [c.value for c in CuisineType]
        for cuisine in v:
            if cuisine not in valid_cuisines:
                raise ValueError(f"Invalid cuisine type: {cuisine}")
        return v
```

---

### 12. Add Caching Layer

**Priority**: Low  
**Effort**: Medium  
**Status**: Not Started

**Description**:  
Add Redis caching for frequently accessed restaurants and dishes.

**Requirements**:
- [ ] Cache popular restaurants (most viewed)
- [ ] Cache restaurant details by ID
- [ ] Cache restaurant lists by city
- [ ] Implement cache invalidation on updates
- [ ] Add cache hit/miss metrics

---

## 📋 Documentation

### 13. Add OpenAPI Examples

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Add comprehensive OpenAPI examples for all endpoints in the interactive docs.

**Requirements**:
- [ ] Add request body examples
- [ ] Add response examples
- [ ] Add example values for all schemas
- [ ] Document error responses

---

### 14. Create Owner/Admin User Guides

**Priority**: Low  
**Effort**: Small  
**Status**: Not Started

**Description**:  
Create guides for restaurant owners and administrators.

**Documents Needed**:
- [ ] Restaurant Owner Guide (how to manage restaurant, add dishes, etc.)
- [ ] Admin Guide (ownership management, moderation)
- [ ] API Integration Guide (for third-party integrations)

---

## ✅ Recently Completed

- [x] Basic CRUD operations for restaurants
- [x] Basic CRUD operations for dishes
- [x] Ownership management system
- [x] Multi-owner support with roles
- [x] Primary ownership transfer
- [x] Archive system integration
- [x] Favorites integration
- [x] Search and filtering
- [x] Authorization (Admin, Owner, Public roles)
- [x] PostgreSQL and SQLite repository implementations
- [x] Comprehensive test coverage (unit, integration, e2e)
- [x] API documentation
- [x] Domain README

---

## 📊 Priority Legend

- 🔴 **Critical**: Blocking issues or security concerns
- 🟡 **High**: Important improvements that impact functionality
- 🟢 **Medium**: Nice-to-have features
- 🔵 **Low**: Minor improvements or polish

---

## 🤝 Contributing

When picking up tasks from this TODO:

1. Update the status to "In Progress"
2. Create a feature branch: `feature/restaurants-{task-name}`
3. Follow the architecture guidelines in ARCHITECTURE.md
4. Write tests (unit + integration + e2e)
5. Update this TODO with any new findings
6. Submit PR for review

---

**Last Updated**: November 2024  
**Next Review**: December 2024

