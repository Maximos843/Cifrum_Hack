import unittest
import logging
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from src.lib.utils.config import Consts
from src.lib.utils.database_client import DatabaseClient, DatabaseClientError

logging.basicConfig(level=logging.ERROR)

class TestDatabaseClient(unittest.TestCase):

    def setUp(self):
        # Reset instances before each test
        DatabaseClient._instances = {}

    def test_singleton_behavior(self):
        # Test that the same instance is returned for the same schema_name
        client1 = DatabaseClient(schema_name='public')
        client2 = DatabaseClient(schema_name='public')
        self.assertIs(client1, client2)

        # Test that different instances are returned for different schema_names
        client3 = DatabaseClient(schema_name='review_schema')
        self.assertIsNot(client1, client3)

    def test_initialize(self):
        # Arrange
        schema_name = 'public'

        # Act
        client = DatabaseClient(schema_name)

        # Assert
        self.assertIsInstance(client.supabase_client, Client)
        self.assertEqual(client.options.schema, schema_name)

    def test_insert_query(self):
        # Arrange
        schema_name = 'public'
        table_name = 'test_table'
        data = {'key': 'value'}

        client = DatabaseClient(schema_name)

        # Act
        client.insert_query(table_name, data)

        # Assert
        response = (
                client.supabase_client.table(table_name)
                .select('key')
                .execute()
            )
        
        self.assertIn(data, response.data)

    def test_insert_query_exception(self):
        # Arrange
        schema_name = 'public'
        table_name = 'nonexistent_table'
        data = {'key': 'value'}

        client = DatabaseClient(schema_name)

        # Act & Assert
        with self.assertRaises(DatabaseClientError) as context:
            client.insert_query(table_name, data)
        self.assertIn(f"Failed to insert data into {table_name}", str(context.exception))

    def test_select_with_condition_query(self):
        # Arrange
        schema_name = 'public'
        table_name = 'test_table'
        column_name = 'key'
        data = 'value'

        client = DatabaseClient(schema_name)

        # Insert test data
        client.insert_query(table_name, {'key': 'value', 'sentiment_text': 'value', 'sentiment_prob': 1})

        # Act
        result = client.select_with_condition_query(table_name, column_name, data)

        # Assert
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn({'sentiment_prob': 1, 'sentiment_text': 'value'}, result)

    def test_select_with_condition_query_exception(self):
        # Arrange
        schema_name = 'public'
        table_name = 'nonexistent_table'
        column_name = 'key'
        data = 'value'

        client = DatabaseClient(schema_name)

        # Act & Assert
        with self.assertRaises(DatabaseClientError) as context:
            client.select_with_condition_query(table_name, column_name, data)
        self.assertIn(f"Failed to select data from {table_name}", str(context.exception))

if __name__ == '__main__':
    unittest.main()