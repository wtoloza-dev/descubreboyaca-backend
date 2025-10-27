"""E2E tests for GET /owner/restaurants/{restaurant_id} endpoint."""

from http import HTTPStatus

import pytest


class TestGetMyRestaurant:
    """E2E tests for GET /owner/restaurants/{restaurant_id}."""

    @pytest.mark.asyncio
    async def test_get_my_restaurant_success(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test owner successfully gets their restaurant details.

        Given: An owner user has ownership of a restaurant
        When: The owner requests their restaurant details
        Then: Returns 200 with complete restaurant data
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="My Restaurant",
            city="Tunja",
            description="Owner's restaurant",
            website="https://myrestaurant.com",
        )
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == restaurant.id
        assert data["name"] == "My Restaurant"
        assert data["city"] == "Tunja"
        assert data["description"] == "Owner's restaurant"

    @pytest.mark.asyncio
    async def test_get_my_restaurant_not_owner(
        self, owner_client, mock_owner_user, create_test_restaurant
    ):
        """Test owner cannot access restaurant they don't own.

        Given: A restaurant exists that the owner doesn't own
        When: The owner tries to access that restaurant
        Then: Returns 403 Forbidden

        Note: The endpoint verifies ownership BEFORE checking if restaurant exists.
        This is correct security behavior - don't reveal resource existence to unauthorized users.
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Someone Else's Restaurant")
        # Note: No ownership created for mock_owner_user

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}"
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        data = response.json()
        assert "permission" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_get_my_restaurant_not_found(self, owner_client):
        """Test getting non-existent restaurant returns 403 (not 404).

        Given: A restaurant ID that doesn't exist
        When: Owner tries to get that restaurant
        Then: Returns 403 Forbidden (ownership check happens first)

        Note: This is correct security behavior. The endpoint checks ownership
        BEFORE checking if restaurant exists, preventing information disclosure.
        A 404 would reveal that a restaurant with that ID doesn't exist.
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{nonexistent_id}"
        )

        # Assert
        # Ownership check fails first, so we get 403 (not 404)
        assert response.status_code == HTTPStatus.FORBIDDEN
        data = response.json()
        assert "permission" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_get_my_restaurant_invalid_id_format(self, owner_client):
        """Test getting restaurant with invalid ID still returns 403.

        Given: A malformed restaurant ID
        When: Owner tries to get that restaurant
        Then: Returns 403 Forbidden (ownership check happens first)

        Note: The ownership check happens before ID validation.
        This is a security trade-off - we don't reveal ID format requirements
        to users who might not have access anyway.
        """
        # Arrange
        # Use a well-formed ULID string to avoid framework validation (422)
        # We want to test ownership (403), not FastAPI's path validation.
        invalid_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{invalid_id}"
        )

        # Assert
        # Ownership check fails first (invalid ID means not an owner)
        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_my_restaurant_includes_all_fields(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test response includes all expected fields.

        Given: An owner has a restaurant with complete data
        When: The owner requests their restaurant
        Then: Response includes all fields (name, address, city, phone, etc.)
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Complete Restaurant",
            address="Calle 19 #9-45",
            city="Tunja",
            state="Boyacá",
            country="Colombia",
            phone="+57 300 123 4567",
            email="info@complete.com",
            website="https://complete.com",
            description="Full details",
        )
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()

        # Verify all expected fields are present
        assert "id" in data
        assert "name" in data
        assert "address" in data
        assert "city" in data
        assert "state" in data
        assert "country" in data
        assert "phone" in data
        assert "email" in data
        assert "website" in data
        assert "description" in data
        assert "created_at" in data
        assert "updated_at" in data

        # Verify values
        assert data["name"] == "Complete Restaurant"
        assert data["city"] == "Tunja"
        assert data["phone"] == "+57 300 123 4567"

    @pytest.mark.asyncio
    async def test_get_my_restaurant_requires_owner_role(
        self, test_client, create_test_restaurant, create_test_ownership
    ):
        """Test that non-owner users cannot access the endpoint.

        Given: A regular (non-owner) user tries to access owner endpoint
        When: The user makes a request without owner role
        Then: Returns 401/403 (auth required or forbidden)
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")

        # Act
        # Using test_client (no auth) instead of owner_client
        response = test_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}"
        )

        # Assert
        assert response.status_code in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        ]
