"""E2E tests for GET /owner/restaurants/ endpoint."""

from http import HTTPStatus

import pytest


class TestListMyRestaurants:
    """E2E tests for GET /owner/restaurants."""

    @pytest.mark.asyncio
    async def test_list_my_restaurants_success(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test owner successfully lists their restaurants.

        Given: An owner has 2 restaurants
        When: The owner requests their restaurant list
        Then: Returns 200 with list of 2 restaurants
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1", city="Tunja")
        restaurant2 = await create_test_restaurant(name="Restaurant 2", city="Sogamoso")

        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant1.id,
            role="owner",
            is_primary=True,
        )
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant2.id,
            role="manager",
            is_primary=False,
        )

        # Act
        response = owner_client.get("/api/v1/restaurants/owner/restaurants")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 2
        assert len(data["items"]) == 2

        # Verify items contain expected fields
        item = data["items"][0]
        assert "restaurant_id" in item
        assert "restaurant_name" in item
        assert "role" in item
        assert "is_primary" in item
        assert "city" in item
        assert "state" in item

    @pytest.mark.asyncio
    async def test_list_my_restaurants_empty(self, owner_client, mock_owner_user):
        """Test owner with no restaurants gets empty list.

        Given: An owner has no restaurants
        When: The owner requests their restaurant list
        Then: Returns 200 with empty list
        """
        # Arrange
        # No restaurants or ownerships created

        # Act
        response = owner_client.get("/api/v1/restaurants/owner/restaurants")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0

    @pytest.mark.asyncio
    async def test_list_my_restaurants_multiple(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test owner with multiple restaurants gets complete list.

        Given: An owner has 4 restaurants with different roles
        When: The owner requests their restaurant list
        Then: Returns 200 with all 4 restaurants
        """
        # Arrange
        restaurants = []
        roles = ["owner", "manager", "staff", "owner"]
        is_primary_flags = [True, False, False, False]

        for i, (role, is_primary) in enumerate(zip(roles, is_primary_flags)):
            restaurant = await create_test_restaurant(
                name=f"Restaurant {i + 1}", city=f"City {i + 1}"
            )
            restaurants.append(restaurant)

            await create_test_ownership(
                owner_id=mock_owner_user.id,
                restaurant_id=restaurant.id,
                role=role,
                is_primary=is_primary,
            )

        # Act
        response = owner_client.get("/api/v1/restaurants/owner/restaurants")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["total"] == 4
        assert len(data["items"]) == 4

        # Verify all restaurant IDs are present
        returned_ids = {item["restaurant_id"] for item in data["items"]}
        expected_ids = {r.id for r in restaurants}
        assert returned_ids == expected_ids

    @pytest.mark.asyncio
    async def test_list_my_restaurants_includes_role_info(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test that response includes role and primary owner status.

        Given: An owner has restaurants with different roles
        When: The owner requests their restaurant list
        Then: Each item includes role and is_primary fields correctly
        """
        # Arrange
        primary_restaurant = await create_test_restaurant(
            name="Primary Restaurant", city="Tunja"
        )
        managed_restaurant = await create_test_restaurant(
            name="Managed Restaurant", city="Sogamoso"
        )

        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=primary_restaurant.id,
            role="owner",
            is_primary=True,
        )
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=managed_restaurant.id,
            role="manager",
            is_primary=False,
        )

        # Act
        response = owner_client.get("/api/v1/restaurants/owner/restaurants")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()

        # Find each restaurant in the response
        items_by_id = {item["restaurant_id"]: item for item in data["items"]}

        # Verify primary restaurant
        primary_item = items_by_id[primary_restaurant.id]
        assert primary_item["role"] == "owner"
        assert primary_item["is_primary"] is True
        assert primary_item["restaurant_name"] == "Primary Restaurant"

        # Verify managed restaurant
        managed_item = items_by_id[managed_restaurant.id]
        assert managed_item["role"] == "manager"
        assert managed_item["is_primary"] is False
        assert managed_item["restaurant_name"] == "Managed Restaurant"

    @pytest.mark.asyncio
    async def test_list_my_restaurants_requires_owner_role(self, test_client):
        """Test that non-owner users cannot access the endpoint.

        Given: A regular (non-owner) user tries to access owner endpoint
        When: The user makes a request without owner role
        Then: Returns 401/403 (auth required or forbidden)
        """
        # Arrange & Act
        # Using test_client (no auth) instead of owner_client
        response = test_client.get("/api/v1/restaurants/owner/restaurants")

        # Assert
        assert response.status_code in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        ]
