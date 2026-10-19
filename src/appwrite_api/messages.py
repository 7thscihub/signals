import os
import traceback
from appwrite.services.messaging import Messaging
from appwrite.id import ID
from .client import get_client
from . import alert_models as am


def send_alert(alert_details: dict = am.SIGNAL_ALERT):
    """Sends a single push notification via Appwrite."""
    alert = am.SignalAlert.model_validate(alert_details)
    client = get_client()
    messaging = Messaging(client)

    response = messaging.create_push(
        message_id=ID.unique(),
        title=alert.title,
        body=alert.body,
        topics=alert.topics,
        data=alert.data
    )
    return response


def get_alert_details(signal: dict):
    """Maps a raw signal dictionary to Appwrite push notification payload format."""
    if not signal:
        return None
    
    title = f"{signal.get('symbol', 'UNKNOWN')} Trade Alert"
    body = f"{signal.get('interval', '')} {signal.get('signal_type', '')}".strip()
    topics = ['mooneazy_signals']
    
    # Ensure all data payload values are strings for Appwrite compatibility
    data = {
        "path": "/",
        "symbol": str(signal.get('symbol', '')),
        "utc_time": str(signal.get('utc_time', ''))
    }
    
    return {"title": title, "body": body, "topics": topics, "data": data}


def send_push_notifications(trade_signals: list[dict], test_alerts=am.SIGNAL_ALERT):
    """Processes a list of trade signals and dispatches push notifications."""
    # Fixed typo: FUNCTION_ENVIRONMENT
   # if not trade_signals and os.environ.get("FUNCTION_ENVIRONMENT", '').lower() != 'dev':
    #     return True

    errors = []
    
    # Safely generate alert details, filtering out invalid/empty signals
    trade_alerts = [get_alert_details(signal) for signal in trade_signals if signal]
    
    # Fallback correctly triggers if the filtered list is empty
    if not trade_alerts:
        trade_alerts = [test_alerts]

    for alert in trade_alerts:
        try:
            send_alert(alert_details=alert)
            print('alert sent')
        except Exception:
            errors.append(traceback.format_exc())
            
    return errors if errors else True

