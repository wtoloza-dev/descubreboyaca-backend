# Workflow Tests - Quick Start Guide

## What Are Workflow Tests?

Workflow tests validate complete application lifecycles using HTTP requests against a running server. They test real-world scenarios from creation through deletion, including cleanup operations.

## Quick Setup

### 1. Start Your Server

```bash
# Terminal 1: Start the development server
make dev
# or
uvicorn app.main:app --reload
```

### 2. Run Workflow Tests

```bash
# Terminal 2: Run workflow tests
make test-workflow
# or
pytest -m workflow -v
```

## Example: Restaurant Lifecycle

The `TestRestaurantLifecycleBasic` test demonstrates a complete workflow:

```
1. CREATE      → Admin creates restaurant
2. FIND ALL    → Verify it appears in listings
3. FIND BY CITY → Verify it appears in city filter  
4. DELETE      → Admin soft-deletes (archives)
5. VERIFY      → Confirm hidden from public queries
6. HARD DELETE → Remove from archive table
7. FINAL CHECK → Confirm complete removal
```

## Running Tests

```bash
# Run all workflow tests
make test-workflow

# Run with minimal output
make test-workflow-fast

# Run specific test
pytest -m workflow tests/workflow/test_restaurant_lifecycle_basic.py -v

# Run specific test method
pytest -m workflow tests/workflow/test_restaurant_lifecycle_basic.py::TestRestaurantLifecycleBasic::test_complete_restaurant_lifecycle -v
```

## Test Against Different Environments

```bash
# Default: localhost
pytest -m workflow

# Staging environment
WORKFLOW_BASE_URL=https://staging.api.example.com pytest -m workflow

# Custom port
WORKFLOW_BASE_URL=http://localhost:8080 pytest -m workflow
```

## Common Issues

### ❌ Connection Refused Error
```
httpx.ConnectError: [Errno 61] Connection refused
```

**Solution**: Make sure the server is running on `localhost:8000`

### ❌ Tests Pass But Leave Data Behind
**Solution**: Check that cleanup code is running (hard delete from archive)

### ❌ Authentication Errors
**Solution**: Currently, workflow tests use test database with auth bypass. For production testing, implement real JWT authentication flow.

## Writing Your First Workflow Test

```python
import pytest
from http import HTTPStatus


@pytest.mark.workflow
class TestMyFeatureLifecycle:
    """Test complete feature lifecycle workflow."""

    @pytest.mark.asyncio
    async def test_my_workflow(
        self,
        workflow_admin_client,
        workflow_http_client,
        workflow_db_session,
    ):
        """Test complete workflow from creation to deletion."""
        
        # 1. Create
        response = await workflow_admin_client.post(
            "/api/v1/my-resource",
            json={"name": "Test Item"}
        )
        assert response.status_code == HTTPStatus.CREATED
        item_id = response.json()["id"]
        
        # 2. Query
        response = await workflow_http_client.get(
            f"/api/v1/my-resource/{item_id}"
        )
        assert response.status_code == HTTPStatus.OK
        
        # 3. Delete
        response = await workflow_admin_client.delete(
            f"/api/v1/my-resource/{item_id}"
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        
        # 4. Cleanup (if needed)
        # Hard delete from archive, etc.
```

## Best Practices

✅ **DO:**
- Mark tests with `@pytest.mark.workflow`
- Clean up all created data (including archives)
- Verify state at each step
- Use descriptive test names
- Document workflow steps in docstrings

❌ **DON'T:**
- Run workflow tests in CI without proper setup
- Use hardcoded IDs that might conflict
- Skip cleanup steps
- Test single operations (use unit/e2e tests instead)
- Leave test data in the database

## Next Steps

1. Read the full documentation: `tests/workflow/README.md`
2. Examine the example test: `tests/workflow/test_restaurant_lifecycle_basic.py`
3. Create your own workflow tests for your features
4. Configure CI/CD to run workflow tests against staging

## Need Help?

- Full documentation: `tests/workflow/README.md`
- Test architecture: `tests/ARCHITECTURE.md`
- Example test: `test_restaurant_lifecycle_basic.py`
- Ask the team in Slack: #backend-tests

