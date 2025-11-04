"""Workflow test for basic restaurant lifecycle.

This module tests the complete lifecycle of a restaurant from creation to
permanent deletion, including verification at each step.

These tests use ONLY HTTP client requests against a running server.
No direct database access is used.

Design Philosophy:
- Test maximum functionality with minimum object creation
- Reuse created objects to test multiple endpoints
- One comprehensive lifecycle test instead of multiple small tests
"""

from http import HTTPStatus

import pytest


@pytest.mark.workflow
class TestRestaurantLifecycleBasic:
    """Test complete restaurant lifecycle workflow.

    This workflow test validates the entire lifecycle using minimal objects:
    - Creates 2 restaurants total (not 4)
    - Tests all major endpoints with these 2 restaurants
    - Verifies data isolation
    - Cleans up properly

    Endpoints tested:
    - POST /admin/ (create)
    - GET /{id} (get by id)
    - GET / (find_all)
    - GET / with filters (find_by_city)
    - DELETE /admin/{id} (soft delete)

    Total: 5 unique endpoint patterns tested with only 2 objects

    Note: Admin UPDATE endpoint does not exist - only owners can update
    """

    @pytest.mark.asyncio
    async def test_complete_restaurant_lifecycle(
        self,
        workflow_admin_client,
        workflow_http_client,
    ):
        """Test complete restaurant lifecycle with maximum endpoint coverage.

        This single test validates the entire lifecycle and multiple endpoints
        using only 2 restaurant objects.

        Workflow Steps:
        1. CREATE: Create 2 restaurants (Tunja and Duitama)
        2. GET BY ID: Retrieve each restaurant individually
        3. FIND ALL: Verify both appear in general listing
        4. FIND BY CITY (Tunja): Test city filter
        5. FIND BY CITY (Duitama): Test city filter
        6. DELETE ONE: Soft-delete Tunja restaurant
        7. VERIFY ISOLATION: Duitama still visible, Tunja not
        8. DELETE OTHER: Soft-delete Duitama restaurant
        9. VERIFY CLEANUP: Neither appears in queries

        Total objects created: 2 restaurants (not 4)
        Total archived records: 2 (not 4)
        Endpoints tested: 6 different endpoints (CRD + filters)

        Note: UPDATE not included - admins cannot update restaurants directly,
        only owners can via update_my_restaurant endpoint
        """
        # ================================================================
        # STEP 1: CREATE 2 RESTAURANTS (Different cities for filter testing)
        # ================================================================
        restaurants_data = [
            {
                "name": "Workflow Restaurant Tunja",
                "description": "Restaurant in Tunja for testing",
                "address": "Calle 19 #10-50",
                "city": "Tunja",
                "province": "Boyacá",
                "phone": "+57 300 111 1111",
                "email": "tunja@workflow.com",
                "latitude": 5.5353,
                "longitude": -73.3678,
                "price_level": 2,
            },
            {
                "name": "Workflow Restaurant Duitama",
                "description": "Restaurant in Duitama for testing",
                "address": "Carrera 20 #15-30",
                "city": "Duitama",
                "province": "Boyacá",
                "phone": "+57 300 222 2222",
                "email": "duitama@workflow.com",
                "latitude": 5.8267,
                "longitude": -73.0339,
                "price_level": 3,
            },
        ]

        restaurant_ids = []
        for restaurant_data in restaurants_data:
            response = await workflow_admin_client.post(
                "/api/v1/restaurants/admin",
                json=restaurant_data,
            )
            assert response.status_code == HTTPStatus.CREATED, (
                f"Failed to create {restaurant_data['name']}: "
                f"{response.status_code} - {response.text}"
            )
            created = response.json()
            restaurant_ids.append(created["id"])
            # Verify response data
            assert created["name"] == restaurant_data["name"]
            assert created["city"] == restaurant_data["city"]

        tunja_id, duitama_id = restaurant_ids
        print(f"Created restaurants: Tunja={tunja_id}, Duitama={duitama_id}")

        # ================================================================
        # STEP 2: GET BY ID (Test individual retrieval)
        # ================================================================
        # Get Tunja restaurant by ID
        tunja_get_response = await workflow_http_client.get(
            f"/api/v1/restaurants/{tunja_id}"
        )
        assert tunja_get_response.status_code == HTTPStatus.OK
        tunja_details = tunja_get_response.json()
        assert tunja_details["id"] == tunja_id
        assert tunja_details["name"] == "Workflow Restaurant Tunja"
        assert tunja_details["city"] == "Tunja"

        # Get Duitama restaurant by ID
        duitama_get_response = await workflow_http_client.get(
            f"/api/v1/restaurants/{duitama_id}"
        )
        assert duitama_get_response.status_code == HTTPStatus.OK
        duitama_details = duitama_get_response.json()
        assert duitama_details["id"] == duitama_id
        assert duitama_details["name"] == "Workflow Restaurant Duitama"
        assert duitama_details["city"] == "Duitama"
        print("✓ GET by ID works for both restaurants")

        # ================================================================
        # STEP 3: VERIFY BOTH IN FIND_ALL
        # ================================================================
        find_all_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"page": 1, "page_size": 100},
        )

        assert find_all_response.status_code == HTTPStatus.OK
        all_restaurants = find_all_response.json()["data"]
        all_ids = [r["id"] for r in all_restaurants]

        # Don't assume exact count, just verify our restaurants are there
        assert len(all_ids) > 0, "find_all should return at least some restaurants"
        assert tunja_id in all_ids, "Tunja restaurant should appear in find_all"
        assert duitama_id in all_ids, "Duitama restaurant should appear in find_all"
        print(f"✓ Both restaurants appear in find_all (total: {len(all_ids)})")

        # ================================================================
        # STEP 4: TEST CITY FILTERS (Tunja)
        # ================================================================
        tunja_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"city": "Tunja", "page": 1, "page_size": 100},
        )

        assert tunja_response.status_code == HTTPStatus.OK
        tunja_restaurants = tunja_response.json()["data"]
        tunja_ids = [r["id"] for r in tunja_restaurants]

        assert tunja_id in tunja_ids, "Tunja restaurant should appear in Tunja filter"
        assert duitama_id not in tunja_ids, (
            "Duitama restaurant should NOT appear in Tunja filter"
        )
        print("✓ Tunja filter works correctly")

        # ================================================================
        # STEP 5: TEST CITY FILTERS (Duitama)
        # ================================================================
        duitama_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"city": "Duitama", "page": 1, "page_size": 100},
        )

        assert duitama_response.status_code == HTTPStatus.OK
        duitama_restaurants = duitama_response.json()["data"]
        duitama_ids = [r["id"] for r in duitama_restaurants]

        assert duitama_id in duitama_ids, (
            "Duitama restaurant should appear in Duitama filter"
        )
        assert tunja_id not in duitama_ids, (
            "Tunja restaurant should NOT appear in Duitama filter"
        )
        print("✓ Duitama filter works correctly")

        # ================================================================
        # STEP 6: DELETE TUNJA RESTAURANT (Test isolation)
        # ================================================================
        delete_tunja_response = await workflow_admin_client.request(
            "DELETE",
            f"/api/v1/restaurants/admin/{tunja_id}",
            json={"note": "Testing delete and isolation"},
        )

        assert delete_tunja_response.status_code == HTTPStatus.NO_CONTENT, (
            f"Failed to delete Tunja restaurant: {delete_tunja_response.status_code}"
        )
        print("✓ Deleted Tunja restaurant")

        # ================================================================
        # STEP 7: VERIFY ISOLATION (Duitama still visible, Tunja not)
        # ================================================================
        # Check find_all
        after_delete_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"page": 1, "page_size": 100},
        )
        assert after_delete_response.status_code == HTTPStatus.OK
        remaining_ids = [r["id"] for r in after_delete_response.json()["data"]]

        assert tunja_id not in remaining_ids, (
            "Deleted Tunja restaurant should not appear"
        )
        assert duitama_id in remaining_ids, "Duitama restaurant should still be present"
        print("✓ Data isolation verified: Tunja deleted, Duitama remains")

        # Verify Tunja filter is empty
        tunja_after_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"city": "Tunja", "page": 1, "page_size": 100},
        )
        tunja_after_ids = [r["id"] for r in tunja_after_response.json()["data"]]
        assert tunja_id not in tunja_after_ids, (
            "Tunja restaurant should not appear in city filter"
        )

        # Verify Duitama filter still works
        duitama_after_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"city": "Duitama", "page": 1, "page_size": 100},
        )
        duitama_after_ids = [r["id"] for r in duitama_after_response.json()["data"]]
        assert duitama_id in duitama_after_ids, "Duitama restaurant should still appear"
        print("✓ City filters work correctly after deletion")

        # ================================================================
        # STEP 8: DELETE DUITAMA RESTAURANT (Cleanup)
        # ================================================================
        delete_duitama_response = await workflow_admin_client.request(
            "DELETE",
            f"/api/v1/restaurants/admin/{duitama_id}",
            json={"note": "Final cleanup"},
        )

        assert delete_duitama_response.status_code == HTTPStatus.NO_CONTENT
        print("✓ Deleted Duitama restaurant")

        # ================================================================
        # STEP 9: VERIFY COMPLETE CLEANUP (Soft Delete)
        # ================================================================
        final_response = await workflow_http_client.get(
            "/api/v1/restaurants",
            params={"page": 1, "page_size": 100},
        )
        final_ids = [r["id"] for r in final_response.json()["data"]]

        assert tunja_id not in final_ids, "Tunja should not appear after cleanup"
        assert duitama_id not in final_ids, "Duitama should not appear after cleanup"
        print("✓ Soft delete verified: Both restaurants removed from active tables")

        # ================================================================
        # STEP 10: HARD DELETE FROM ARCHIVES (Complete Cleanup)
        # ================================================================
        # Clean up Tunja restaurant from archive
        cleanup_tunja_response = await workflow_admin_client.request(
            "DELETE",
            "/api/v1/audit/admin/archives",
            json={
                "original_table": "restaurants",
                "original_id": tunja_id,
            },
        )
        assert cleanup_tunja_response.status_code == HTTPStatus.OK, (
            f"Failed to hard delete Tunja from archive: "
            f"{cleanup_tunja_response.status_code} - {cleanup_tunja_response.text}"
        )
        tunja_cleanup = cleanup_tunja_response.json()
        assert tunja_cleanup["success"] is True
        print("✓ Hard deleted Tunja restaurant from archive")

        # Clean up Duitama restaurant from archive
        cleanup_duitama_response = await workflow_admin_client.request(
            "DELETE",
            "/api/v1/audit/admin/archives",
            json={
                "original_table": "restaurants",
                "original_id": duitama_id,
            },
        )
        assert cleanup_duitama_response.status_code == HTTPStatus.OK, (
            f"Failed to hard delete Duitama from archive: "
            f"{cleanup_duitama_response.status_code} - {cleanup_duitama_response.text}"
        )
        duitama_cleanup = cleanup_duitama_response.json()
        assert duitama_cleanup["success"] is True
        print("✓ Hard deleted Duitama restaurant from archive")

        # ================================================================
        # SUCCESS: Complete lifecycle validated with full cleanup
        # ================================================================
        print("✅ Complete restaurant lifecycle test passed!")
        print("   - Created: 2 restaurants")
        print("   - Tested: CRD + filters + isolation (no U - admin can't update)")
        print("   - Endpoints: POST, GET, GET (filters), DELETE")
        print("   - Soft deleted: 2 records (archived)")
        print("   - Hard deleted: 2 records (permanently removed)")
        print("   - Efficiency: 5 endpoints with only 2 objects")
        print("   - Cleanup: Complete (no test data persists)")
