"""Workflow tests package.

This package contains end-to-end workflow tests that test complete application
lifecycles using HTTP client against a running server instance.

Key characteristics:
- Tests complete user/business workflows from start to finish
- Uses HTTP client (not TestClient) against localhost or real URLs
- Tests data persistence and state across multiple operations
- Includes database verification at different stages
- Tests cleanup operations including hard deletes from archive tables

These tests are marked with @pytest.mark.workflow and are excluded from
regular test runs by default. To run them:

    pytest -m workflow

Note: These tests require the application to be running or use fixtures
that start the application.
"""
