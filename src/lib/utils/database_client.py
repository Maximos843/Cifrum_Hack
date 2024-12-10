import logging
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

from src.lib.utils.config import Consts

logging.basicConfig(level=logging.ERROR)


class DatabaseClientError(Exception):
    """Custom exception for DatabaseClient errors."""
    pass


class DatabaseClient:
    _instances = {}

    def __new__(cls, schema_name: str):
        if schema_name not in cls._instances:
            cls._instances[schema_name] = super(DatabaseClient, cls).__new__(cls)
            cls._instances[schema_name].initialize(schema_name)
        return cls._instances[schema_name]

    def initialize(self, schema_name: str):
        try:
            self.options = ClientOptions().replace(schema=schema_name)
            self.supabase_client: Client = create_client(
                Consts.SUPABASE_URL, Consts.SUPABASE_KEY, options=self.options
            )
        except Exception as e:
            logging.error(f"Error occurred in initializing Supabase client: {e}")
            raise DatabaseClientError(f"Failed to initialize Supabase client: {e}")

    def insert_query(self, table_name: str, data: dict) -> None:
        try:
            response = (
                self.supabase_client.table(table_name)
                .insert(data)
                .execute()
            )
            logging.info(f"Data inserted into {table_name}: {data}")
        except Exception as e:
            logging.error(f"Error occurred in insert_query: {e}")
            raise DatabaseClientError(f"Failed to insert data into {table_name}: {e}")

    def select_with_condition_query(self, table_name: str, column_name: str, data: str) -> str | None:
        try:
            response = (
                self.supabase_client.table(table_name)
                .select('sentiment_prob, sentiment_text')
                .eq(column_name, data)
                .execute()
            )

            return response.data
        except Exception as e:
            logging.error(f"Error occurred in select_with_condition_query: {e}")
            raise DatabaseClientError(f"Failed to select data from {table_name}: {e}")
