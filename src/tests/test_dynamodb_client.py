# tests/test_dynamodb_client.py
import unittest
from moto import mock_aws
import boto3
from dynamodb.client import DynamoDBClient


@mock_aws
class TestDynamoDBClient(unittest.TestCase):

    def setUp(self):
        self.dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
        self.table_name = "test-table"
        self.table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        self.table.meta.client.get_waiter("table_exists").wait(
            TableName=self.table_name
        )

        self.client = DynamoDBClient(
            table_name=self.table_name,
            region_name="us-west-2",
            app_key="fake-key",
            app_token="fake-token",
        )

    def tearDown(self):
        self.table.delete()
        self.table.meta.client.get_waiter("table_not_exists").wait(
            TableName=self.table_name
        )

    def test_put_item(self):
        item = {"id": "123", "name": "test"}
        result = self.client.put_item(item)
        self.assertEqual(result, "Success")

    def test_get_item(self):
        item = {"id": "123", "name": "test"}
        self.client.put_item(item)
        result = self.client.get_item({"id": "123"})
        self.assertEqual(result, item)

    def test_scan_table(self):
        item = {"id": "123", "name": "test"}
        self.client.put_item(item)
        result = self.client.scan_table()
        self.assertEqual(result, [item])

    def test_update_item(self):
        item = {"id": "123", "name": "test"}
        self.client.put_item(item)
        update_expression = "SET #name = :value"
        expression_attribute_values = {":value": "updated"}
        expression_attribute_names = {"#name": "name"}
        result = self.client.update_item(
            key={"id": "123"},
            update_expression=update_expression,
            expression_attribute_values=expression_attribute_values,
            expression_attribute_names=expression_attribute_names,
        )
        self.assertEqual(result, "Success")

    def test_delete_item(self):
        item = {"id": "123", "name": "test"}
        self.client.put_item(item)
        result = self.client.delete_item({"id": "123"})
        self.assertEqual(result, "Success")


if __name__ == "__main__":
    unittest.main()
