# Users Domain (Admin Only)

## Overview

The **Users** domain provides administrative user management endpoints. This domain is separated from the `auth` domain to maintain clear boundaries:

- **`auth` domain**: Authentication, registration, login, token management
- **`users` domain**: User CRUD operations for administrators

## Architecture

```
app/domains/users/
├── routes/
│   └── admin/          # Admin-only endpoints
│       ├── create.py   # POST /api/v1/users/admin - Create user
│       ├── find_all.py # GET /api/v1/users/admin - List users
│       └── delete.py   # DELETE /api/v1/users/admin/{id} - Delete user
├── services/
│   └── user.py         # UserService - Business logic
├── schemas/
│   └── admin/          # Request/Response schemas
│       ├── create.py
│       ├── find_all.py
│       └── delete.py
└── dependencies/
    └── user.py         # Dependency injection

```

## Endpoints

All endpoints require **ADMIN** role.

### 1. Create User
```http
POST /api/v1/users/admin
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "newuser@example.com",
  "full_name": "New User",
  "password": "SecurePassword123!",
  "role": "user",
  "is_active": true
}
```

**Response: 201 Created**
```json
{
  "id": "01K96CK8FC6C4YBH2180KEK255",
  "email": "newuser@example.com",
  "full_name": "New User",
  "role": "user",
  "is_active": true,
  "created_at": "2025-01-15T10:30:00Z"
}
```

### 2. Find All Users
```http
GET /api/v1/users/admin?page=1&page_size=20
Authorization: Bearer {admin_token}
```

**Response: 200 OK**
```json
{
  "data": [
    {
      "id": "01K96CK8FC6C4YBH2180KEK255",
      "email": "john.doe@example.com",
      "full_name": "John Doe",
      "role": "admin",
      "is_active": true,
      "auth_provider": "email",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1
  }
}
```

### 3. Delete User
```http
DELETE /api/v1/users/admin/{user_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "note": "User requested account deletion"
}
```

**Response: 204 No Content**

## Soft Delete with Archive

When a user is deleted:
1. ✅ User data is saved to the `archive` table with metadata
2. ✅ User is removed from the `users` table
3. ✅ Operation is atomic (both succeed or both fail)

Archive entry includes:
- Original user data (JSON)
- Deletion timestamp
- Admin who performed deletion
- Optional note explaining why

## Usage in Workflow Tests

This domain is essential for workflow tests:

```python
# Create test users dynamically
response = await workflow_admin_client.post(
    "/api/v1/users/admin",
    json={
        "email": "testowner@example.com",
        "full_name": "Test Owner",
        "password": "TestPassword123!",
        "role": "owner",
        "is_active": True,
    },
)
owner_id = response.json()["id"]

# ... use owner_id for ownership tests ...

# Clean up after test
await workflow_admin_client.request(
    "DELETE",
    f"/api/v1/users/admin/{owner_id}",
    json={"note": "Workflow test cleanup"},
)
```

## Dependencies

- **UserRepository** (from `auth` domain): User persistence
- **ArchiveRepository** (from `audit` domain): Archive persistence
- **PasswordHasher** (from `auth` domain): Password hashing

## Design Decisions

### Why Separate from `auth`?

- **Single Responsibility**: `auth` focuses on authentication; `users` focuses on management
- **Security**: User management is admin-only; auth is public
- **Testability**: Easier to test admin operations independently
- **Scalability**: Can add more admin operations without bloating auth domain

### Why Reuse `auth` Repositories?

- **DRY**: Avoid duplicating repository code
- **Consistency**: Same data access patterns
- **Maintainability**: Single source of truth for user data

## Future Enhancements

Possible additions:
- `GET /admin/{id}` - Get user by ID
- `PATCH /admin/{id}` - Update user details
- `PATCH /admin/{id}/role` - Change user role
- `PATCH /admin/{id}/activate` - Activate/deactivate user
- Bulk operations (bulk create, bulk delete)
- User activity logs
- Password reset (admin-initiated)

## Related Domains

- **`auth`**: User authentication, registration, login
- **`audit`**: Archive system for deleted records
- **`restaurants`**: Restaurant ownership (uses users)

