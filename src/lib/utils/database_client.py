import os
from dotenv import load_dotenv
from supabase import create_client, Client,
from supabase.lib.client_options import ClientOptions



class DatabaseClient:
    def __init__(self, schema_name: str) -> None:
        # here better use Consts class from Maxs PR
        # is it good idea to throw exceptions in __init__
        try:
            load_dotenv()
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            self.options = ClientOptions().replace(schema=schema_name)
            self.supabase_client: Client = create_client(url, key, options=self.options)
        except Exception as e:
            print(f"Error occurred in init_supabse_client: {e}")
            
    def insert_query(self, table_name: str, data: dict) -> None:
        response = (
            self.supabase_client.table(table_name)
            .insert(data)
            .execute()
        )
        
    def select_with_condition_query(self, table_name: str, column_name: str, data: str) -> str | None:
        response = (
            self.supabase_client.table(table_name)
            .select('*')
            .eq(column_name, data)
            .execute()
        )
        
        return response.data

