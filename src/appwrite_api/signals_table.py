import os
from collections.abc import Callable
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
    def __init__(self, db_client=get_db_client, database_id = DATABASE_ID, table_id = TABLE_ID):
        self.tablesDB = db_client()
        self.database_id = database_id
        self.table_id = table_id
    
    @validate_call
    def add_signal(self, data: SignalData) -> dict:
        row = self.tablesDB.create_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=ID.unique(),
            data=data.model_dump(),
        )
        return row.model_dump()

    def add_signals(self, signals):
        new_signals = []
        for signal in signals:
            new_signal = self.add_signal(signal)
            new_signals.append(new_signal)
        return new_signals

    def get_signal(self, signal_id: str) -> dict:
        row = self.tablesDB.get_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=signal_id,
        )
        return row.model_dump()

    @validate_call
    def update_signal(self, signal:SignalModel) -> dict:
        row = self.tablesDB.update_row(
            database_id=self.database_id,
            table_id=self.table_id,
            row_id=signal.id,
            data=signal.data.model_dump()
        )
        return row.model_dump()
    
    def update_signals(self, signals:list[dict]):
        for signal in signals:
            self.update_signal(signal_dict=signal)

    def get_closed_signals(self, limit=10) ->list[dict]:
        response = self.tablesDB.list_rows(
            database_id=self.database_id,
            table_id=self.table_id,
            queries=[
                Query.equal("status", 'closed'),
                Query.order_asc("$createdAt"),
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



