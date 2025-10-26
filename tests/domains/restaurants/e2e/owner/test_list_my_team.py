"""E2E tests for GET /owner/restaurants/{restaurant_id}/team endpoint."""

from http import HTTPStatus

import pytest


class TestListMyTeam:
    """E2E tests for GET /owner/restaurants/{restaurant_id}/team."""

    @pytest.mark.asyncio
    async def test_list_my_team_success(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test owner successfully lists team members.

        Given: An owner has a restaurant with 3 team members
        When: The owner requests the team list
        Then: Returns 200 with list of 3 team members
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Team Restaurant")

        # Create ownership for the requesting owner
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )

        # Create additional team members
        from app.shared.domain.factories import generate_ulid

        owner2_id = generate_ulid()
        owner3_id = generate_ulid()

        await create_test_ownership(
            owner_id=owner2_id, restaurant_id=restaurant.id, role="manager"
        )
        await create_test_ownership(
            owner_id=owner3_id, restaurant_id=restaurant.id, role="staff"
        )

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/team"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "team" in data
        assert "total" in data
        assert "restaurant_id" in data
        assert data["restaurant_id"] == restaurant.id
        assert data["total"] == 3
        assert len(data["team"]) == 3

        # Verify team members have expected fields
        member = data["team"][0]
        assert "owner_id" in member
        assert "role" in member
        assert "is_primary" in member

    @pytest.mark.asyncio
    async def test_list_my_team_not_owner(
        self, owner_client, mock_owner_user, create_test_restaurant
    ):
        """Test owner cannot view team of restaurant they don't own.

        Given: A restaurant exists that the owner doesn't own
        When: The owner tries to view that restaurant's team
        Then: Returns 403 Forbidden
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Someone Else's Restaurant")
        # Note: No ownership created for mock_owner_user

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/team"
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN
        data = response.json()
        assert "permission" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_list_my_team_not_found(self, owner_client):
        """Test viewing team of non-existent restaurant returns 403.

        Given: A restaurant ID that doesn't exist
        When: Owner tries to view team
        Then: Returns 403 Forbidden (ownership check happens first)

        Note: Similar to get_my_restaurant, ownership is verified first
        before checking if restaurant exists.
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{nonexistent_id}/team"
        )

        # Assert
        # Ownership check fails first, so we get 403 (not 404)
        assert response.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_list_my_team_multiple_members(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test restaurant with multiple team members returns all.

        Given: A restaurant has 5 team members with different roles
        When: The owner requests the team list
        Then: Returns all 5 team members with correct roles
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Large Team Restaurant")

        # Create ownerships for 5 team members
        from app.shared.domain.factories import generate_ulid

        team_members = [
            (mock_owner_user.id, "owner", True),  # Primary owner
            (generate_ulid(), "owner", False),  # Secondary owner
            (generate_ulid(), "manager", False),
            (generate_ulid(), "manager", False),
            (generate_ulid(), "staff", False),
        ]

        for owner_id, role, is_primary in team_members:
            await create_test_ownership(
                owner_id=owner_id,
                restaurant_id=restaurant.id,
                role=role,
                is_primary=is_primary,
            )

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/team"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["total"] == 5
        assert len(data["team"]) == 5

        # Verify all owner IDs are present
        returned_ids = {member["owner_id"] for member in data["team"]}
        expected_ids = {owner_id for owner_id, _, _ in team_members}
        assert returned_ids == expected_ids

        # Verify roles
        roles_count = {}
        for member in data["team"]:
            role = member["role"]
            roles_count[role] = roles_count.get(role, 0) + 1

        assert roles_count["owner"] == 2
        assert roles_count["manager"] == 2
        assert roles_count["staff"] == 1

    @pytest.mark.asyncio
    async def test_list_my_team_primary_marked_correctly(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test that primary owner is marked correctly in team list.

        Given: A restaurant has a primary owner and other team members
        When: The owner requests the team list
        Then: Only one member has is_primary=True
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Restaurant with Primary")

        from app.shared.domain.factories import generate_ulid

        owner2_id = generate_ulid()
        owner3_id = generate_ulid()

        # Create primary owner
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )

        # Create non-primary members
        await create_test_ownership(
            owner_id=owner2_id,
            restaurant_id=restaurant.id,
            role="manager",
            is_primary=False,
        )
        await create_test_ownership(
            owner_id=owner3_id,
            restaurant_id=restaurant.id,
            role="staff",
            is_primary=False,
        )

        # Act
        response = owner_client.get(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/team"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()

        # Count primary owners
        primary_count = sum(1 for member in data["team"] if member["is_primary"])
        assert primary_count == 1

        # Find the primary owner and verify it's the current user
        primary_member = next(member for member in data["team"] if member["is_primary"])
        assert primary_member["owner_id"] == mock_owner_user.id
        assert primary_member["role"] == "owner"

    @pytest.mark.asyncio
    async def test_list_my_team_requires_owner_role(
        self, test_client, create_test_restaurant
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
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/team"
        )

        # Assert
        assert response.status_code in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
        ]
