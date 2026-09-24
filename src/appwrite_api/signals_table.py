import os
from collections.abc import Callable
from pydantic import validate_call
from appwrite.client import Client
from appwrite.id import ID
from appwrite.services.tables_db import TablesDB
from appwrite.query import Query
from appwrite.exception import AppwriteException
from .models import SignalModel, ResultModel, SignalData, ResultData 


DATABASE_ID = os.environ.get("SIGNALS_DB_ID")
TABLE_ID = os.environ.get("SIGNALS_TABLE_ID")
SIGNALS_LIMIT = 10
TEST_SIGNAL_ID = '6ab244cc00375e76cf65'

@validate_call()
def get_db_client()->TablesDB:
    client = Client()
    client.set_endpoint(os.environ.get("APPWRITE_FUNCTION_API_ENDPOINT"))
    client.set_project(os.environ.get("APPWRITE_FUNCTION_PROJECT_ID"))
    client.set_key(os.environ.get("APPWRITE_FUNCTION_API_KEY"))
    return TablesDB(client)


class SignalsTable:
    def __init__(self, database_client=get_db_client, database_id=DATABASE_ID, table_id=TABLE_ID):
        self.tablesDB = database_client()
        self.database_id = database_id
        self.table_id = table_id

    def add_signal(self, data: dict) -> dict:
        row = self.tablesDB.create_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=ID.unique(),
            data=data,
        )
        return row.model_dump()
    
    def get_signal(self, signal_id: str) -> dict:
        row = self.tablesDB.get_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=signal_id,
        )
        return row.model_dump()

    def get_pending_signal(self, signal_id):
        signal = self.get_signal(signal_id)
        if signal['data']['status'] != 'pending': 
            return []
        return signal

    def update_signal(self, signal_dict) -> dict:
        row = self.tablesDB.update_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=signal_dict['id'],
            data=signal_dict['data'],
        )
        return row.model_dump()
    
    def update_signals(self, signals:list[dict]):
        for signal in signals:
            self.update_signal(signal_dict)

    def get_closed_signals(self, limit=10) ->list[dict]:
        response = self.tablesDB.list_rows(
            database_id=self.database_id,
            table_id=self.table_id,
            queries=[
                Query.equal("status", 'closed'),
                Query.limit(limit)
            ]
        )
        rows = response.rows
        return [row.to_dict() for row in rows]

    def get_pending_signals(self, limit=10):
        response = self.tablesDB.list_rows(
            database_id=self.database_id,
            table_id=self.table_id,
            queries=[
                Query.equal("status", 'pending'),
                Query.order_asc("$createdAt"),
                Query.limit(limit)
            ]
        )
        rows = response.rows
        return [row.to_dict() for row in rows]



