"""Tests package for the application.

This package contains all tests organized by domain and type.

Test Organization:
------------------

1. Unit Tests (tests/domains/*/unit/)
   - Test individual components in isolation
   - Fast execution, no external dependencies
   - Focus on business logic and domain entities

2. Integration Tests (tests/domains/*/integration/)
   - Test component interactions (repositories, services)
   - Use test database but mock external services
   - Focus on data persistence and service layer logic

3. E2E Tests (tests/domains/*/e2e/)
   - Test complete API endpoints using TestClient
   - Use test database with dependency overrides
   - Focus on HTTP request/response validation

4. Workflow Tests (tests/workflow/)
   - Test complete application lifecycles
   - Use HTTP client against running server (localhost)
   - Test real-world workflows from creation to deletion
   - Include hard delete verification from archive tables
   - Marked with @pytest.mark.workflow
   - NOT run by default (must use: pytest -m workflow)

Running Tests:
--------------

All tests except workflow:
    pytest

Only workflow tests:
    pytest -m workflow

Specific test type:
    pytest tests/domains/restaurants/unit/
    pytest tests/domains/restaurants/integration/
    pytest tests/domains/restaurants/e2e/

With coverage:
    pytest --cov=app --cov-report=html
"""
