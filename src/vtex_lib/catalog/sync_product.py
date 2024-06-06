from src.vtex_lib.sync_client import SyncVtexClient
from typing import Any


class SyncProductAPI:
    def __init__(self, client: SyncVtexClient) -> None:
        self.client: SyncVtexClient = client

    def get_product(self, account_name: str, environment: str, product_id: str) -> Any:
        endpoint: str = (
            f"{account_name}.{environment}.com.br/api/catalog/pvt/product/{product_id}"
        )
        return self.client._requests("GET", endpoint=endpoint)
