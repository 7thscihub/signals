from .appwrite_api.db import update_signals
from .appwrite_api.messages import send_push_notifications
import traceback
from mooneazy.scripts.scalper import get_scalping_signals

def main(context):
    errors = {}
    latest_signals = []
    try:
        signals, scalper_errors = get_scalping_signals()
        errors['scalper_errors'] = scalper_errors or None
    except Exception as e:
        context.log(traceback.format_exc())
        if signals:
        try:
            send_push_notifications(signals)
        except Exception as e:
            errors['push_notification_errors'] = e
            context.log(traceback.format_exc())
    try:
        # update signals database and return latest_signals
        db_signals, db_errors = update_signals(signals)
        if db_signals:
            latest_signals = db_signals
        errors['updated_signals_errors'] = db_errors or None

    except Exception as e:
        context.log(traceback.format_exc())

    return context.res.json({
        "signals": latest_signals or signals,
        "errors": errors if errors else None 
    })




