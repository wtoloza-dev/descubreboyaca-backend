# Workflow Tests

Workflow tests validate complete application lifecycles by testing real-world user scenarios from start to finish. Unlike unit, integration, or e2e tests, workflow tests simulate actual usage patterns including creation, querying, updates, deletion, and cleanup operations.

## Key Characteristics

- **End-to-End Workflows**: Test complete business processes, not individual operations
- **HTTP Client**: Use `httpx.AsyncClient` to make real HTTP requests against a running server
- **State Verification**: Verify database state at multiple points in the workflow
- **Real-World Scenarios**: Simulate actual user behavior patterns
- **Cleanup Testing**: Include hard delete operations from archive tables
- **Isolated Execution**: Do not run with regular test suite by default

## When to Use Workflow Tests

Use workflow tests for:

- ✅ Complete lifecycle testing (create → use → delete → cleanup)
- ✅ Multi-step user journeys
- ✅ Validating data consistency across operations
- ✅ Testing archive and cleanup processes
- ✅ Integration scenarios across multiple domains
- ✅ Smoke testing against deployed environments

Do NOT use workflow tests for:

- ❌ Testing individual business rules (use unit tests)
- ❌ Testing repository or service methods (use integration tests)
- ❌ Testing endpoint validation (use e2e tests)
- ❌ Fast feedback during development (use unit/integration tests)

## Running Workflow Tests

### Prerequisites

For localhost testing, ensure the application is running:

```bash
# Start the application (in a separate terminal)
uvicorn app.main:app --reload
```

Or use the application's startup fixtures (to be implemented).

### Running Tests

```bash
# Run all workflow tests
pytest -m workflow

# Run specific workflow test
pytest -m workflow tests/workflow/test_restaurant_lifecycle_basic.py

# Run with verbose output
pytest -m workflow -v

# Run all tests INCLUDING workflow tests
pytest -m ""
```

### Testing Against Different Environments

By default, workflow tests run against `http://localhost:8000`. You can override this using the `WORKFLOW_BASE_URL` environment variable:

```bash
# Test against localhost (default)
pytest -m workflow

# Test against staging
WORKFLOW_BASE_URL=https://staging.api.descubreboyaca.com pytest -m workflow

# Test against production (use with caution!)
WORKFLOW_BASE_URL=https://api.descubreboyaca.com pytest -m workflow
```

⚠️ **Warning**: When testing against real environments, be aware that:
- Tests will create, modify, and delete real data
- Use test-specific data that can be safely cleaned up
- Consider using separate test databases for staging environments

## Writing Workflow Tests

### Basic Structure

```python
"""Workflow test for [feature] lifecycle."""

import pytest
from http import HTTPStatus
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.[domain].models import [Model]


@pytest.mark.workflow
class Test[Feature]Lifecycle:
    """Test complete [feature] lifecycle workflow."""

    @pytest.mark.asyncio
    async def test_complete_[feature]_lifecycle(
        self,
        workflow_admin_client,
        workflow_http_client,
        workflow_db_session: AsyncSession,
    ):
        """Test complete lifecycle from creation to hard delete.

        Workflow Steps:
        1. CREATE: [description]
        2. QUERY: [description]
        3. UPDATE: [description]
        4. DELETE: [description]
        5. CLEANUP: [description]
        """
        # Step 1: Create
        create_response = await workflow_admin_client.post(...)
        assert create_response.status_code == HTTPStatus.CREATED
        item_id = create_response.json()["id"]

        # Step 2: Query and verify
        get_response = await workflow_http_client.get(...)
        assert get_response.status_code == HTTPStatus.OK

        # Step 3: Update
        update_response = await workflow_admin_client.patch(...)
        assert update_response.status_code == HTTPStatus.OK

        # Step 4: Delete (soft delete)
        delete_response = await workflow_admin_client.delete(...)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        # Verify archived
        result = await workflow_db_session.exec(
            select(ArchiveModel).where(...)
        )
        archive = result.first()
        assert archive is not None

        # Step 5: Hard delete from archive
        await workflow_db_session.delete(archive)
        await workflow_db_session.commit()

        # Final verification
        result = await workflow_db_session.exec(
            select(ArchiveModel).where(...)
        )
        assert result.first() is None
```

### Available Fixtures

#### `workflow_base_url`
Returns the base URL for API requests (default: `http://localhost:8000`).

```python
def test_example(workflow_base_url: str):
    print(f"Testing against: {workflow_base_url}")
```

#### `workflow_http_client`
Async HTTP client for making unauthenticated requests.

```python
@pytest.mark.asyncio
async def test_example(workflow_http_client):
    response = await workflow_http_client.get("/api/v1/restaurants")
    assert response.status_code == 200
```

#### `workflow_admin_client`
Async HTTP client with admin authentication (to be fully implemented).

```python
@pytest.mark.asyncio
async def test_example(workflow_admin_client):
    response = await workflow_admin_client.delete("/api/v1/restaurants/admin/123")
    assert response.status_code == 204
```

#### `workflow_db_session`
Database session for direct state verification.

```python
@pytest.mark.asyncio
async def test_example(workflow_db_session: AsyncSession):
    result = await workflow_db_session.exec(
        select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
    )
    restaurant = result.first()
    assert restaurant is not None
```

## Example: RestaurantLifecycleBasic

The `TestRestaurantLifecycleBasic` class demonstrates a complete workflow test:

1. **Create**: Admin creates a restaurant via POST `/api/v1/restaurants/admin`
2. **Query All**: Verify restaurant appears in GET `/api/v1/restaurants`
3. **Query by City**: Verify restaurant appears in city-filtered query
4. **Delete**: Admin soft-deletes restaurant (archives it)
5. **Verify Hidden**: Confirm restaurant no longer appears in public queries
6. **Hard Delete**: Remove from archive table via direct database operation
7. **Final Verification**: Confirm complete removal from system

This test validates:
- Restaurant creation and persistence
- Public query functionality (find_all, find_by_city)
- Soft delete with archiving
- Archive data integrity
- Hard delete cleanup
- Data isolation between operations

## Best Practices

### 1. Clear Workflow Steps
```python
# Good: Clear sections with comments
# ================================================================
# STEP 1: CREATE RESTAURANT
# ================================================================
create_response = await workflow_admin_client.post(...)

# Bad: All operations without structure
create_response = await workflow_admin_client.post(...)
get_response = await workflow_http_client.get(...)
delete_response = await workflow_admin_client.delete(...)
```

### 2. Verify State at Each Step
```python
# Good: Verify database state matches expectations
create_response = await workflow_admin_client.post(...)
assert create_response.status_code == 201

result = await workflow_db_session.exec(...)
assert result.first() is not None

# Bad: Only check HTTP responses
create_response = await workflow_admin_client.post(...)
assert create_response.status_code == 201
```

### 3. Clean Up After Tests
```python
# Good: Hard delete archives at the end
await workflow_db_session.delete(archive)
await workflow_db_session.commit()

# Bad: Leave test data in archive table
pass  # Don't clean up
```

### 4. Test Data Isolation
```python
# Good: Use unique identifiers per test
restaurant_data = {
    "name": f"Workflow Test {uuid4()}",
    "email": f"test-{timestamp}@workflow.com",
}

# Bad: Use hardcoded values that might conflict
restaurant_data = {
    "name": "Test Restaurant",
    "email": "test@workflow.com",
}
```

### 5. Descriptive Assertions
```python
# Good: Clear assertion messages
assert restaurant_id in all_ids, "Restaurant should appear in find_all"

# Bad: Bare assertions
assert restaurant_id in all_ids
```

## Troubleshooting

### Tests fail with connection errors
- Ensure the application is running on the expected URL
- Check `WORKFLOW_BASE_URL` environment variable
- Verify network connectivity to target server

### Tests pass but data persists
- Ensure cleanup code is running (check for early returns)
- Verify hard delete operations are executed
- Check for transaction commit issues

### Authentication errors
- Workflow fixtures currently use test database auth bypass
- For real server testing, implement proper authentication flow
- Consider using test user credentials stored securely

### Database verification fails
- Ensure `workflow_db_session` points to the same database as the server
- Check for transaction isolation issues
- Verify session commits are happening

## Future Enhancements

- [ ] Auto-start application for workflow tests
- [ ] Real JWT authentication flow for admin client
- [ ] Support for owner and user client fixtures
- [ ] Cleanup hooks to prevent test data leakage
- [ ] Performance monitoring for workflow operations
- [ ] Support for testing against containerized environments
- [ ] Workflow test templates/generators
- [ ] Integration with CI/CD for smoke testing

## Related Documentation

- [Tests Architecture](../ARCHITECTURE.md) - Overall test organization
- [E2E Tests](../domains/restaurants/e2e/) - Endpoint-level testing
- [Integration Tests](../domains/restaurants/integration/) - Service/repository testing
- [Unit Tests](../domains/restaurants/unit/) - Component-level testing

