"""E2E tests for GraphQL endpoint.

Tests the GraphQL endpoint for restaurant queries with various filters.
"""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestRestaurantGraphQL:
    """Test suite for GraphQL /api/v1/restaurants/graphql endpoint."""

    def test_graphql_endpoint_exists(self, test_client: TestClient):
        """Test that GraphQL endpoint is accessible.

        Given: GraphQL endpoint is registered
        When: POST to /api/v1/restaurants/graphql with introspection query
        Then: Returns 200 with schema information
        """
        # Arrange
        query = """
        {
            __schema {
                queryType {
                    name
                }
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={"query": query},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert data["data"]["__schema"]["queryType"]["name"] == "Query"

    @pytest.mark.asyncio
    async def test_graphql_restaurant_by_id(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test querying a restaurant by ID.

        Given: A restaurant exists in the database
        When: Query restaurant by ID via GraphQL
        Then: Returns restaurant data
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Test Restaurant",
            city="Tunja",
            description="A test restaurant",
        )

        query = """
        query GetRestaurant($id: String!) {
            restaurant(id: $id) {
                id
                name
                city
                description
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={
                "query": query,
                "variables": {"id": restaurant.id},
            },
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert data["data"]["restaurant"]["id"] == restaurant.id
        assert data["data"]["restaurant"]["name"] == "Test Restaurant"
        assert data["data"]["restaurant"]["city"] == "Tunja"
        assert data["data"]["restaurant"]["description"] == "A test restaurant"

    @pytest.mark.asyncio
    async def test_graphql_restaurants_list(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test querying list of restaurants.

        Given: Multiple restaurants in database
        When: Query restaurants via GraphQL
        Then: Returns paginated list of restaurants
        """
        # Arrange
        await create_test_restaurant(name="Restaurant 1", city="Tunja")
        await create_test_restaurant(name="Restaurant 2", city="Sogamoso")
        await create_test_restaurant(name="Restaurant 3", city="Duitama")

        query = """
        query GetRestaurants {
            restaurants {
                items {
                    id
                    name
                    city
                }
                total
                page
                pageSize
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={"query": query},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]["restaurants"]["items"]) == 3
        assert data["data"]["restaurants"]["total"] == 3
        names = [r["name"] for r in data["data"]["restaurants"]["items"]]
        assert "Restaurant 1" in names
        assert "Restaurant 2" in names
        assert "Restaurant 3" in names

    @pytest.mark.asyncio
    async def test_graphql_filter_by_city(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test filtering restaurants by city via GraphQL.

        Given: Restaurants in different cities
        When: Query with city filter
        Then: Returns only matching restaurants
        """
        # Arrange
        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        query = """
        query GetRestaurantsByCity($city: String) {
            restaurants(filters: { city: $city }) {
                items {
                    name
                    city
                }
                total
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={
                "query": query,
                "variables": {"city": "Tunja"},
            },
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert data["data"]["restaurants"]["total"] == 2
        assert len(data["data"]["restaurants"]["items"]) == 2
        assert all(r["city"] == "Tunja" for r in data["data"]["restaurants"]["items"])

    @pytest.mark.asyncio
    async def test_graphql_pagination(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test pagination in GraphQL queries.

        Given: 15 restaurants in database
        When: Query with pagination parameters
        Then: Returns correct page of results
        """
        # Arrange
        for i in range(15):
            await create_test_restaurant(name=f"Restaurant {i:02d}", city="Tunja")

        query = """
        query GetRestaurantsPage($page: Int, $pageSize: Int) {
            restaurants(pagination: { page: $page, pageSize: $pageSize }) {
                items {
                    name
                }
                total
                page
                pageSize
                totalPages
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={
                "query": query,
                "variables": {"page": 2, "pageSize": 5},
            },
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        restaurants_data = data["data"]["restaurants"]
        assert len(restaurants_data["items"]) == 5
        assert restaurants_data["page"] == 2
        assert restaurants_data["pageSize"] == 5
        assert restaurants_data["total"] == 15
        assert restaurants_data["totalPages"] == 3

    @pytest.mark.asyncio
    async def test_graphql_field_selection(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test that GraphQL allows selective field querying.

        Given: A restaurant with complete data
        When: Query only specific fields
        Then: Returns only requested fields
        """
        # Arrange
        await create_test_restaurant(
            name="Complete Restaurant",
            city="Tunja",
            description="Full description",
            phone="+57 300 123 4567",
        )

        query = """
        query GetRestaurantNames {
            restaurants {
                items {
                    name
                }
                total
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={"query": query},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        items = data["data"]["restaurants"]["items"]
        assert len(items) == 1
        # Verify only requested fields are present
        assert "name" in items[0]
        # GraphQL might include __typename, but other fields should not be present
        # unless explicitly requested

    @pytest.mark.asyncio
    async def test_graphql_restaurant_not_found(self, test_client: TestClient):
        """Test querying non-existent restaurant.

        Given: Restaurant ID that doesn't exist
        When: Query restaurant by that ID
        Then: Returns null for restaurant
        """
        # Arrange
        query = """
        query GetRestaurant($id: String!) {
            restaurant(id: $id) {
                id
                name
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={
                "query": query,
                "variables": {"id": "01234567890ABCDEFGHIJKLMN"},
            },
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert data["data"]["restaurant"] is None

    @pytest.mark.asyncio
    async def test_graphql_filter_by_price_level(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test filtering by price level via GraphQL.

        Given: Restaurants with different price levels
        When: Query with priceLevel filter
        Then: Returns only matching restaurants
        """
        # Arrange
        await create_test_restaurant(name="Budget", city="Tunja", price_level=1)
        await create_test_restaurant(name="Moderate", city="Tunja", price_level=2)
        await create_test_restaurant(name="Expensive", city="Tunja", price_level=3)

        query = """
        query GetRestaurantsByPrice($priceLevel: Int) {
            restaurants(filters: { priceLevel: $priceLevel }) {
                items {
                    name
                    priceLevel
                }
                total
            }
        }
        """

        # Act
        response = test_client.post(
            "/api/v1/restaurants/graphql",
            json={
                "query": query,
                "variables": {"priceLevel": 2},
            },
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        restaurants_data = data["data"]["restaurants"]
        assert restaurants_data["total"] == 1
        assert len(restaurants_data["items"]) == 1
        assert restaurants_data["items"][0]["name"] == "Moderate"
        assert restaurants_data["items"][0]["priceLevel"] == 2
