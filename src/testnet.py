from .mooneazy.mooneazy.scripts.scalper import scalper_debugger
import json
import traceback


if __name__ == '__main__':
    print("scalper_debugger running")
    scalper_debugger()



def get_pending_signals():
    tablesDB = getTable()
    signals = {}
    pending_tp1 = tablesDB.list_rows(
        database_id=DATABASE_ID,
        table_id=TABLE_ID,
        queries=[ Query.not_equal("tp1", "success") ]
    )

    pending_tp2 = tablesDB.list_rows(
        database_id=DATABASE_ID,
        table_id=TABLE_ID,
        queries=[ Query.not_equal("tp2", "success")]
    )

    # Combine rows while avoiding duplicates
    combined_rows = tp1_response["rows"] + tp2_response["rows"]
    rows = { row["$id"]: row for row in }

    return list(rows.values())
