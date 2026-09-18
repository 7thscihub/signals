import traceback
import mooneazy.trading.results import get_results
from .appwrite.db import upddate_results, get_pending_signals
from .appwrite_api.messages import send_push_notifications


def main(context):
    new_results = []

    try:
        pending_signals = get_pending_signals()
        results = get_results(pending_signals)
        send_push_notifications(results)
        upddate_results(results)
    except Exception as e:
        context.log(traceback.format_exc(e))

    return latest updated results

