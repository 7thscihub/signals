import traceback
from mooneazy.trading.results import get_updated_signals
from .appwrite_api.db import update_results, get_pending_signals
from .appwrite_api.messages import send_push_notifications


def main(context):
    new_results = []
    errors = None
    try:
        pending_signals = get_pending_signals()
        updated_signals = get_updated_signals(pending_signals)
        if updated_signals:
            send_push_notifications(updated_signals)
            upddate_results(updated_signals)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
    if errors:
        return context.res.json({'errors': errors})
    return context.res.json(new_results)

