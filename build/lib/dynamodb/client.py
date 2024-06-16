# src/dynamodb_client.py

from typing import Optional, Dict, List
import boto3
from botocore.exceptions import ClientError


class DynamoDBClient:
    """A client to interact with Amazon DynamoDB.

    This client provides methods to perform operations on a specified DynamoDB table.
    """

    def __init__(
        self, table_name: str, region_name: str, app_key: str, app_token: str
    ) -> None:
        """Initializes a connection to a specified DynamoDB table.

        Args:
            table_name (str): The name of the DynamoDB table.
            region_name (str): The AWS region where the DynamoDB table is located.
            app_key (str): The AWS access key ID.
            app_token (str): The AWS secret access key.
        """
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=region_name,
            aws_access_key_id=app_key,
            aws_secret_access_key=app_token,
        )
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, key: Dict) -> Optional[Dict]:
        """Retrieves an item from the DynamoDB table using a provided key.

        Args:
            key (dict): The key of the item to retrieve.

        Returns:
            dict | None: The retrieved item, or None if the item could not be retrieved.
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item", {})
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def scan_table(self) -> Optional[List[Dict]]:
        """Scans the entire DynamoDB table and retrieves all items.

        Returns:
            list | None: A list of all items in the table, or None if the scan failed.
        """
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def put_item(self, item: Dict) -> Optional[str]:
        """Adds a new item to the DynamoDB table.

        Args:
            item (dict): The item to add.

        Returns:
            str | None: "Success" if the item was added successfully,
            or None if the operation failed.
        """
        try:
            self.table.put_item(Item=item)
            return "Success"
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def update_item(
        self,
        key: Dict,
        update_expression: str,
        expression_attribute_values: Dict,
        expression_attribute_names: Optional[Dict] = None,
    ) -> Optional[str]:
        """Updates an existing item in the DynamoDB table.

        Args:
            key (dict): The key of the item to update.
            update_expression (str): A string representing the update to perform.
            expression_attribute_values (dict): A dictionary of attribute values for the update.
            expression_attribute_names (dict): A dictionary of attribute names for the update.

        Returns:
            str | None: "Success" if the item was updated successfully,
            or None if the operation failed.
        """
        try:
            update_kwargs = {
                "Key": key,
                "UpdateExpression": update_expression,
                "ExpressionAttributeValues": expression_attribute_values,
            }
            if expression_attribute_names:
                update_kwargs["ExpressionAttributeNames"] = expression_attribute_names

            self.table.update_item(**update_kwargs)
            return "Success"
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None

    def delete_item(self, key: Dict) -> Optional[str]:
        """Deletes an item from the DynamoDB table.

        Args:
            key (dict): The key of the item to delete.

        Returns:
            str | None: "Success" if the item was deleted successfully,
            or None if the operation failed.
        """
        try:
            self.table.delete_item(Key=key)
            return "Success"
        except ClientError as e:
            print(e.response["Error"]["Message"])
            return None
