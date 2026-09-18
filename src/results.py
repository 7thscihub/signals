import traceback
from mooneazy.trading.results import get_results
from .appwrite_api.db import upddate_results, get_pending_signals
from .appwrite_api.messages import send_push_notifications


def main(context):
    new_results = []
    errors = None
    try:
        pending_signals = get_pending_signals()
        new_results = get_results(pending_signals)
        send_push_notifications(results)
        upddate_results(results)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
    if erros:
        return context.res(errors)
    return context.res(new_results)

