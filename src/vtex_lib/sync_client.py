"""File to start SyncVtexClient class"""

from typing import Dict, Any
from enum import Enum
import requests
from requests import Response


class HttpMethod(Enum):
    """
    Enumeration for HTTP methods.

    Attributes:
        GET (str): Represents the GET HTTP method.
        POST (str): Represents the POST HTTP method.
        PUT (str): Represents the PUT HTTP method.
        DELETE (str): Represents the DELETE HTTP method.
        PATCH (str): Represents the PATCH HTTP method.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class SyncVtexClient:
    """
    Synchronous client for interacting with VTEX API.

    Attributes:
        base_url (str): The base URL for the VTEX API.
        headers (Dict[str, str]): The headers used for authentication with the VTEX API.
    """

    def __init__(self, base_url: str, app_key: str, app_token: str) -> None:
        """
        Initializes the SyncVtexClient with the base URL, app key, and app token.

        Args:
            base_url (str): The base URL for the VTEX API.
            app_key (str): The application key for VTEX API authentication.
            app_token (str): The application token for VTEX API authentication.
        """
        self.base_url: str = base_url
        self.headers: Dict[str, str] = {
            "X-VTEX-API-AppKey": app_key,
            "X-VTEX-API-AppToken": app_token,
        }

    def _requests(self, method: HttpMethod, endpoint: str, **kwargs) -> Any:
        """
        Makes an HTTP request to the VTEX API.

        Args:
            method (HttpMethod): The HTTP method to use for the request (GET, POST, PUT, DELETE, PATCH).
            endpoint (str): The endpoint path for the request.
            **kwargs: Additional arguments passed to the requests.request method (e.g., params, data, json).

        Returns:
            Any: The JSON response from the VTEX API.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url: str = f"{self.base_url}/{endpoint}"
        response: Response = requests.request(
            method=method.value, url=url, headers=self.headers, timeout=5, **kwargs
        )
        response.raise_for_status()
        return response.json()
