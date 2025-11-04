"""Workflow tests package.

This package contains end-to-end workflow tests that test complete application
lifecycles using HTTP client against a running server instance.

Key characteristics:
- Tests complete user/business workflows from start to finish
- Uses HTTP client (not TestClient) against localhost or real URLs
- Tests data persistence and state across multiple operations
- Tests cleanup operations using hard delete endpoint
- Admin tools for user management in multi-role workflows

These tests are marked with @pytest.mark.workflow and are excluded from
regular test runs by default. To run them:

    pytest -m workflow

Available cleanup tools:
- DELETE /api/v1/archives - Hard delete archived records
- POST/GET/DELETE /api/v1/users/admin - Manage test users

Documentation:
- README.md - Complete workflow testing guide
- CLEANUP_GUIDE.md - Hard delete and user management examples
- SUMMARY.md - Implementation status and test results

Note: These tests require the application to be running or use fixtures
that start the application.
"""
