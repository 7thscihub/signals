import os
from .appwrite_api.signals_table import SignalsTable 
from .appwrite_api.messages import send_push_notifications
import traceback
from mooneazy.scripts.scalper import get_scalping_signals


def main(context):
    signals = []
    errors = {}
    latest_signals = []

    try:
        signals = get_scalping_signals()
    except Exception as e:
        errors['scalper_errors'] = traceback.format_exc()
        context.log(errors)

    try:
        # update signals database and return latest_signals
        latest_signals = SignalsTable().add_signals(signals)
    except Exception as e:
        errors['db errors'] = traceback.format_exc()
        context.log(traceback.format_exc()) 

    try:
        send_push_notifications(latest_signals)
    except Exception as e:
        errors['push_notification_errors'] = e
        context.log(traceback.format_exc())

    try:
        return context.res.json({
            "signals": latest_signals or signals,
            "errors": f"{errors}" if errors else None 
        })
    except TypeError as e:
        context.log(traceback.format_exc())
        return context.res.json({
            'errors': "json encoding error"
        })



