# Workflow Test Cleanup Guide

This guide demonstrates how to use the hard delete endpoint and user management tools to properly clean up after workflow tests.

## Hard Delete Endpoint

The hard delete endpoint (`DELETE /api/v1/audit/admin/archives`) permanently removes archived records from the database. Use this at the end of workflow tests to ensure no test data persists.

### Basic Usage

```python
import pytest
from http import HTTPStatus


@pytest.mark.workflow
class TestWithCleanup:
    """Example workflow test with proper cleanup."""

    @pytest.mark.asyncio
    async def test_complete_lifecycle_with_cleanup(
        self,
        workflow_admin_client,
        workflow_http_client,
    ):
        """Test complete lifecycle including hard delete cleanup."""
        
        # ================================================================
        # STEP 1: CREATE RESOURCE
        # ================================================================
        create_response = await workflow_admin_client.post(
            "/api/v1/restaurants/admin",
            json={
                "name": "Test Restaurant for Cleanup",
                "email": "cleanup-test@example.com",
                "phone": "+573001234567",
                "address": "Test Address 123",
                "city": "Tunja",
                "category": "COLOMBIAN",
                "price_range": "MEDIUM",
            },
        )
        assert create_response.status_code == HTTPStatus.CREATED
        restaurant_id = create_response.json()["id"]
        
        # ================================================================
        # STEP 2: PERFORM OPERATIONS
        # ================================================================
        # ... your test operations here ...
        
        # ================================================================
        # STEP 3: SOFT DELETE (ARCHIVE)
        # ================================================================
        delete_response = await workflow_admin_client.delete(
            f"/api/v1/restaurants/admin/{restaurant_id}",
            json={"note": "Workflow test cleanup"},
        )
        assert delete_response.status_code == HTTPStatus.NO_CONTENT
        
        # ================================================================
        # STEP 4: HARD DELETE FROM ARCHIVE
        # ================================================================
        cleanup_response = await workflow_admin_client.request(
            "DELETE",
            "/api/v1/audit/admin/archives",
            json={
                "original_table": "restaurants",
                "original_id": restaurant_id,
            },
        )
        
        # Verify cleanup was successful
        assert cleanup_response.status_code == HTTPStatus.OK
        cleanup_data = cleanup_response.json()
        assert cleanup_data["success"] is True
        assert "permanently deleted" in cleanup_data["message"]
```

## User Management for Multi-User Workflows

When testing workflows that involve multiple user roles (admin, owner, user), use the user management endpoints to create and clean up test users.

### Creating Test Users

```python
@pytest.mark.workflow
class TestMultiUserWorkflow:
    """Example workflow test with multiple users."""

    @pytest.mark.asyncio
    async def test_owner_workflow(
        self,
        workflow_admin_client,
        workflow_http_client,
    ):
        """Test workflow involving owner and admin users."""
        
        # ================================================================
        # STEP 1: CREATE TEST OWNER USER
        # ================================================================
        create_owner_response = await workflow_admin_client.post(
            "/api/v1/users/admin",
            json={
                "email": "testowner@workflow-cleanup.com",
                "password": "SecureTestPass123!",
                "full_name": "Test Owner for Cleanup",
                "role": "OWNER",
                "is_active": True,
            },
        )
        assert create_owner_response.status_code == HTTPStatus.CREATED
        owner_user_id = create_owner_response.json()["id"]
        
        # ================================================================
        # STEP 2: AUTHENTICATE AS OWNER
        # ================================================================
        # Create authenticated client for owner
        import httpx
        import os
        
        base_url = os.getenv("WORKFLOW_BASE_URL", "http://localhost:8000")
        
        # Login as owner
        async with httpx.AsyncClient(base_url=base_url) as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                json={
                    "email": "testowner@workflow-cleanup.com",
                    "password": "SecureTestPass123!",
                },
            )
            assert login_response.status_code == HTTPStatus.OK
            owner_token = login_response.json()["access_token"]
        
        # Create owner client
        async with httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {owner_token}"},
        ) as owner_client:
            # ================================================================
            # STEP 3: PERFORM OWNER OPERATIONS
            # ================================================================
            # ... owner creates restaurant, manages dishes, etc. ...
            
            pass  # Your test logic here
        
        # ================================================================
        # STEP 4: CLEANUP - DELETE USER (SOFT DELETE)
        # ================================================================
        delete_user_response = await workflow_admin_client.delete(
            f"/api/v1/users/admin/{owner_user_id}",
            json={"note": "Workflow test user cleanup"},
        )
        assert delete_user_response.status_code == HTTPStatus.NO_CONTENT
        
        # ================================================================
        # STEP 5: CLEANUP - HARD DELETE USER FROM ARCHIVE
        # ================================================================
        cleanup_user_response = await workflow_admin_client.request(
            "DELETE",
            "/api/v1/audit/admin/archives",
            json={
                "original_table": "users",
                "original_id": owner_user_id,
            },
        )
        assert cleanup_user_response.status_code == HTTPStatus.OK
        assert cleanup_user_response.json()["success"] is True
```

## Cleanup Helper Function

You can create a reusable cleanup helper to avoid repetition:

```python
from typing import Literal


async def cleanup_archived_record(
    admin_client,
    table: Literal["restaurants", "users", "dishes", "reviews"],
    record_id: str,
) -> None:
    """Hard delete a record from archive table.
    
    Args:
        admin_client: Authenticated admin HTTP client
        table: Name of the original table
        record_id: ULID of the record to delete
        
    Raises:
        AssertionError: If cleanup fails
    """
    response = await admin_client.request(
        "DELETE",
        "/api/v1/audit/admin/archives",
        json={
            "original_table": table,
            "original_id": record_id,
        },
    )
    
    assert response.status_code == HTTPStatus.OK, (
        f"Failed to cleanup {table} record {record_id}: "
        f"{response.status_code} - {response.text}"
    )
    
    data = response.json()
    assert data["success"] is True, (
        f"Cleanup reported failure: {data.get('message')}"
    )


# Usage in tests:
@pytest.mark.workflow
class TestWithHelper:
    """Example using cleanup helper."""

    @pytest.mark.asyncio
    async def test_with_cleanup_helper(
        self,
        workflow_admin_client,
    ):
        """Test using reusable cleanup helper."""
        
        # Create and use restaurant
        create_response = await workflow_admin_client.post(...)
        restaurant_id = create_response.json()["id"]
        
        # ... test operations ...
        
        # Soft delete
        await workflow_admin_client.delete(
            f"/api/v1/restaurants/admin/{restaurant_id}",
            json={"note": "Test cleanup"},
        )
        
        # Hard delete using helper
        await cleanup_archived_record(
            workflow_admin_client,
            "restaurants",
            restaurant_id,
        )
```

**Note**: Remember to use `.request("DELETE", url, json=...)` instead of `.delete(url, json=...)` as httpx's delete method doesn't accept json parameter:

```python
# Correct - using request()
await client.request("DELETE", "/api/v1/audit/admin/archives", json={...})

# Wrong - will cause TypeError
await client.delete("/api/v1/audit/admin/archives", json={...})
```

### Helper Function Example

Here's the complete helper function with correct syntax:

```python
from typing import Literal
from http import HTTPStatus


async def cleanup_archived_record(
    admin_client,
    table: Literal["restaurants", "users", "dishes", "reviews"],
    record_id: str,
) -> None:
    """Hard delete a record from archive table."""
    response = await admin_client.request(
        "DELETE",
        "/api/v1/audit/admin/archives",
        json={
            "original_table": table,
            "original_id": record_id,
        },
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["success"] is True
```

## Batch Cleanup

For tests that create multiple resources, clean them up in a structured way:

```python
@pytest.mark.workflow
class TestBatchCleanup:
    """Example with batch cleanup of multiple resources."""

    @pytest.mark.asyncio
    async def test_multiple_resources_cleanup(
        self,
        workflow_admin_client,
    ):
        """Test creating and cleaning up multiple resources."""
        
        created_resources = {
            "restaurants": [],
            "users": [],
            "dishes": [],
        }
        
        try:
            # ================================================================
            # CREATE MULTIPLE RESOURCES
            # ================================================================
            # Create test owner
            owner_response = await workflow_admin_client.post(
                "/api/v1/users/admin",
                json={...},
            )
            owner_id = owner_response.json()["id"]
            created_resources["users"].append(owner_id)
            
            # Create restaurants
            for i in range(3):
                restaurant_response = await workflow_admin_client.post(
                    "/api/v1/restaurants/admin",
                    json={...},
                )
                restaurant_id = restaurant_response.json()["id"]
                created_resources["restaurants"].append(restaurant_id)
            
            # ================================================================
            # PERFORM TEST OPERATIONS
            # ================================================================
            # ... your test logic here ...
            
        finally:
            # ================================================================
            # CLEANUP - SOFT DELETE ALL RESOURCES
            # ================================================================
            # Delete restaurants
            for restaurant_id in created_resources["restaurants"]:
                await workflow_admin_client.delete(
                    f"/api/v1/restaurants/admin/{restaurant_id}",
                    json={"note": "Batch cleanup"},
                )
            
            # Delete users
            for user_id in created_resources["users"]:
                await workflow_admin_client.delete(
                    f"/api/v1/users/admin/{user_id}",
                    json={"note": "Batch cleanup"},
                )
            
            # ================================================================
            # CLEANUP - HARD DELETE FROM ARCHIVES
            # ================================================================
            # Clean restaurants from archive
            for restaurant_id in created_resources["restaurants"]:
                await cleanup_archived_record(
                    workflow_admin_client,
                    "restaurants",
                    restaurant_id,
                )
            
            # Clean users from archive
            for user_id in created_resources["users"]:
                await cleanup_archived_record(
                    workflow_admin_client,
                    "users",
                    user_id,
                )
```

## Best Practices

### 1. Always Clean Up in `finally` Blocks

```python
# Good: Cleanup happens even if test fails
try:
    # Test operations
    pass
finally:
    # Cleanup
    await cleanup_archived_record(...)

# Bad: Cleanup might not happen if test fails
# Test operations
await cleanup_archived_record(...)
```

### 2. Track Created Resources

```python
# Good: Track all created resources for cleanup
created_ids = []
for data in test_data:
    response = await client.post(...)
    created_ids.append(response.json()["id"])

# Clean all
for record_id in created_ids:
    await cleanup_archived_record(...)

# Bad: Lose track of created resources
await client.post(...)
await client.post(...)
# How do we clean up? Lost the IDs!
```

### 3. Verify Cleanup Success

```python
# Good: Verify each cleanup operation
response = await client.delete("/api/v1/archives", json={...})
assert response.status_code == HTTPStatus.OK
assert response.json()["success"] is True

# Bad: Don't verify cleanup
await client.delete("/api/v1/archives", json={...})
# Did it work? We don't know!
```

### 4. Use Descriptive Notes

```python
# Good: Clear note for audit trail
await client.delete(
    f"/api/v1/users/admin/{user_id}",
    json={"note": "Workflow test cleanup: test_owner_workflow"},
)

# Bad: Generic or missing note
await client.delete(
    f"/api/v1/users/admin/{user_id}",
    json={"note": "cleanup"},
)
```

## Troubleshooting

### Cleanup Returns 404

**Problem**: Hard delete returns 404 Not Found

**Solution**: The record might not have been soft-deleted first. Ensure:
1. The resource was soft-deleted before trying to hard delete
2. The `original_table` name matches exactly (e.g., "restaurants", not "restaurant")
3. The `original_id` is the correct ULID

### Cleanup Returns 401/403

**Problem**: Authentication error during cleanup

**Solution**: Ensure you're using `workflow_admin_client` which has admin authentication. Hard delete requires admin privileges.

### Resources Not Found After Test

**Problem**: Can't find resources to clean up

**Solution**: Always store IDs immediately after creation:
```python
response = await client.post(...)
resource_id = response.json()["id"]  # Store immediately
```

## Related Documentation

- [Workflow Tests README](README.md) - Main workflow testing guide
- [Workflow Tests Summary](SUMMARY.md) - Implementation summary
- [Archive System](../../app/domains/audit/) - Audit and archive system details

---

**Last Updated**: November 4, 2025
**Test Framework**: pytest + httpx
**Python Version**: 3.12+

