import os
import copy
from appwrite.client import Client
from appwrite.id import ID
from appwrite.services.tables_db import TablesDB
from appwrite.query import Query


DATABASE_ID = os.environ.get("SIGNALS_DB_ID")
TABLE_ID = os.environ.get("SIGNALS_TABLE_ID")
SIGNALS_LIMIT = 10

def get_client():
    client = Client()
    client.set_endpoint(os.environ.get("APPWRITE_FUNCTION_API_ENDPOINT"))
    client.set_project(os.environ.get("APPWRITE_FUNCTION_PROJECT_ID"))
    client.set_key(os.environ.get("APPWRITE_FUNCTION_API_KEY"))
    return client


def get_latest_signals(table, limit=10):
    response = table.list_rows(
        database_id=DATABASE_ID,
        table_id=TABLE_ID,
        queries=[
            Query.order_desc("$createdAt"),
            Query.limit(limit)
        ]
    )
    rows = getattr(response, "rows", [])
    return [row.to_dict() for row in rows]


def update_signals(signals):
    if not signals:
        return None, None
    signals_copy = copy.deepcopy(signals)
    appwrite_client = get_client()
    signals_table = TablesDB(appwrite_client)

    for signal in signals_copy:
        try:
            signal_id = ID.unique()
            signals_table.create_row(
                database_id=DATABASE_ID,
                table_id=TABLE_ID,
                row_id=signal_id,
                data=signal
            )
        except AppwriteException as e:
            if e.code == 409:
                continue
            else:
                errors.append(e)

    latest_signals = get_latest_signals(table=signals_table, limit=SIGNALS_LIMIT) or None
    return latest_signals, errors


