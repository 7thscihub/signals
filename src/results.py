import traceback
from mooneazy.trading.results import get_updated_signals
from .appwrite_api.db import update_results, get_pending_signals
from .appwrite_api.messages import send_push_notifications


def main(context):
    # return context.res.json({'status:': "called"})
    results = {
        "pending_signals": None,
        "updated_signals": None,
        "errors": None
    }
    try:
        pending_signals = get_pending_signals()
        results['pending_signals'] = pending_signals
        updated_signals = get_updated_signals(pending_signals)
        
        if updated_signals:
            results['updated_signals'] = updated_signals
            send_push_notifications(updated_signals)
            upddate_results(updated_signals)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
        results['errors'] = errors
    return context.res.json(results)


