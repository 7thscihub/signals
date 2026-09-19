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


@validate_call()
def get_db_client()->TablesDB:
    client = Client()
    client.set_endpoint(os.environ.get("APPWRITE_FUNCTION_API_ENDPOINT"))
    client.set_project(os.environ.get("APPWRITE_FUNCTION_PROJECT_ID"))
    client.set_key(os.environ.get("APPWRITE_FUNCTION_API_KEY"))
    return TablesDB(client)


def get_cleaned_signals(signals):
    clean_signals = []
    for signal in signals:
        valid_siganl = SignalData.model_validate(signal)
        clean_signals.append(valid_siganl.model_dump())
    return clean_signals


def get_valid_results(results: list[dict]) -> tuple:
    valid_results = []
    errors = []
    for result in results:
        try:
            valid_result.append(ResultData.model_validate(result))
        except Exception as e:
            errors.append(traceback.format_exc(e))
            continue
    return valid_results, errors


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


def get_row(db_client: Callable, database_id, table_id, row_id):
    result = db_client().get_row(
        database_id=database_id,
        table_id=table_id,
        row_id=row_id
    )


@validate_call()
def update_row(
        db_client: Callable, 
        database_id: str, 
        table_id: str , 
        row_id: str, 
        row_data: dict
    ):
    result = db_client().update_row(
        database_id=database_id,
        table_id=table_id,
        row_id=row_id,
        data=SignalData.model_validate(row_data).model_dump()
    )


@validate_call()
def create_row(
        db_client: Callable, 
        db_id: str, 
        table_id: str, 
        row_id: str, 
        row_data: dict
    ):
    response = db_client().create_row(
        database_id=db_id,
        table_id=table_id,
        row_id=row_id ,
        data=SignalData.model_validate(row_data).model_dump()
    )


def update_signals(signals: list[dict]):
    if not signals:
        return

    clean_signals = get_cleaned_signals(signals)
    signals_table = get_db_client()
    errors = []
    for signal in clean_signals:
        try:
            signal_id = ID.unique()
            signals_table.create_row(
                database_id=DATABASE_ID,
                table_id=TABLE_ID,
                row_id=signal_id,
                data=signal
            )
        except AppwriteException as e:
            # skipping duplicate if sigal exists
            if e.code == 409:
                continue
            else:
                errors.append(e)


@validate_call(validate_return=True)
def get_latest_results(
        db_client: Callable = get_db_client, 
        database_id: str = DATABASE_ID, 
        table_id: str = TABLE_ID,
        limit: int = 10
    )->list[dict]:

    response = db_client().list_rows(
        database_id=database_id,
        table_id=table_id,
        queries=[
            Query.or_([
                Query.equal("tp1_results", "fail"),
                Query.equal("tp2_results", "fail"),
                Query.equal("tp1_results", "success"),
                Query.equal("tp2_results", "success")
            
            ]),
            Qwery.limit(limit)
        ]
    )
    rows = response.get("rows", [])
    return [row.to_dict() for row in rows]


@validate_call(validate_return=True)
def get_pending_signals(
        db_client: Callable = get_db_client, 
        database_id: str = DATABASE_ID, 
        table_id: str = TABLE_ID
    )->dict[str, dict] | None:
    """
    returns signals that have not hit a stop loss or all its tps
    checks for a null or pending status for either of the tps
    """
    tablesDB = db_client()
    pending_tp1 = tablesDB.list_rows(
        database_id=DATABASE_ID,
        table_id=TABLE_ID,
        queries=[ Query.not_equal("tp1_results", "success") ]
    )

    pending_tp2 = tablesDB.list_rows(
        database_id=DATABASE_ID,
        table_id=TABLE_ID,
        queries=[ Query.not_equal("tp2_results", "success")]
    )

    # Combine rows while avoiding duplicates
    combined_rows = pending_tp1["rows"] + pending_tp2["rows"]
    rows = { row["$id"]: row['data'] for row in combined_rows}
    return rows or None 



def update_results(results):
    valid_results, errors = get_valid_results(results)
    if not valid_results:
        return

    for result in valid_results:
        update_row(
            db_client=get_db_client,
            database_id=DATABASE_ID,
            table_id=TABLE_ID,
            row_id=results.signal_id,
            row_data={
                'tp1_results': result.tp1_results,
                'tp2_results': result.tp2_results,
            }
        )
    return valid_results, errors




