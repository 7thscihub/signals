import traceback
from mooneazy.trading.results import get_new_results
from .appwrite_api.signals_table import SignalsTable
from .appwrite_api.messages import send_push_notifications

TEST_SIGNAL_ID = '6ab244cc00375e76cf65'


def main(context):
    signal_id = context.req.query.get('id')
    table = SignalsTable()
    pending_signals = []
    results = []
    errors = []

    try:
        if not signal_id:
            pending_signals = table.get_pending_signals()
        else:
            pending_signals.append(
                table.get_pending_signal(signal_id=signal_id)
            )
        results = get_new_results(pending_signals)
        table.update_signals(results)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
        return context.res.json(errors)
    return context.res.json(results)


