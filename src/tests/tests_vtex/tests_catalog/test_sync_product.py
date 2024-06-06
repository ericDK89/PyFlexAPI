"""File to handle all tests for SyncProductAPI class"""

from unittest.mock import patch
from typing import Any
import pytest
from src.vtex_lib.sync_client import SyncVtexClient
from src.vtex_lib.catalog.sync_product import SyncProductAPI


@pytest.fixture
def client() -> SyncVtexClient:
    """
    Fixture for creating a SyncVtexClient instance with predefined credentials.

    Returns:
        SyncVtexClient: An instance of SyncVtexClient initialized with test credentials.
    """
    return SyncVtexClient(
        base_url="https://api.vtex.com",
        app_key="app_key",
        app_token="app_token",
    )


@pytest.fixture
def product_api(client: SyncVtexClient) -> SyncProductAPI:
    """
    Fixture for creating a SyncProductAPI instance using the provided SyncVtexClient.

    Args:
        client (SyncVtexClient): An instance of SyncVtexClient.

    Returns:
        SyncProductAPI: An instance of SyncProductAPI initialized with the provided client.
    """
    return SyncProductAPI(client)


@patch("vtex_lib.sync_client.requests.request")
def test_get_product(mock_request, product_api: SyncProductAPI) -> None:
    """
    Test the get_product method of SyncProductAPI.

    This test mocks the requests.request method to simulate a successful API response
    and verifies that the get_product method returns the expected result and makes
    the correct API call.

    Args:
        mock_request (unittest.mock.Mock): Mock object for requests.request.
        product_api (SyncProductAPI): An instance of SyncProductAPI to be tested.

    Asserts:
        The response from get_product matches the expected result.
        The requests.request method is called once with the correct parameters.
    """

    # * Configuring the mock to return a successful response
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"id": "123", "name": "Produto Teste"}

    # * Calling the method to be tested
    response: Any = product_api.get_product("account_name", "environment", "123")

    # * Asserting the response
    assert response == {"id": "123", "name": "Produto Teste"}

    # * Asserting that the request was made with the correct parameters
    mock_request.assert_called_once_with(
        "GET",
        "https://api.vtex.com/account_name.environment.com.br/api/catalog/pvt/product/123",
        headers={
            "X-VTEX-API-AppKey": "app_key",
            "X-VTEX-API-AppToken": "app_token",
        },
    )
