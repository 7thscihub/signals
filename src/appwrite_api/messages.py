import os
import traceback
from appwrite.services.messaging import Messaging
from appwrite.id import ID
from .client import get_client
from . import alert_models as am


def send_alert(alert_details:dict):
    """Sends a single push notification via Appwrite."""
    alert = am.SignalAlert.model_validate(alert_details)
    client = get_client()
    messaging = Messaging(client)

    response = messaging.create_push(
        message_id=ID.unique(),
        title=alert.title,
        body=alert.body,
        topics=alert.topics,
        data=alert.data.model_dump()
    )
    return response


def get_alert_details(signal: dict):
    """
    Maps a raw signal dictionary to Appwrite push notification payload format.
    """
    signal_id = signal.get('id')
    if signal_id:
        signal = signal['data'] | { 'id': signal_id }
    title = f"{signal.get('symbol', 'UNKNOWN')} Trade Alert"
    body = f"{signal.get('interval', '')} {signal.get('signal_type', '')}".strip()
    topics = ['mooneazy_signals']
    
    data = {
        "path": "/",
        "symbol": str(signal.get('symbol', '')),
        "utc_time": str(signal.get('utc_time', '')),
        "signal_type": signal["signal_type"],
        "id": signal.get('id', "")
    }
 
    return {"title": title, "body": body, "topics": topics, "data": data}


def send_push_notifications(latest_signals: list[dict]=[], test_alert=am.SIGNAL_ALERT):
    """Processes a list of trade signals and dispatches push notifications."""

    errors = []
    trade_alerts = []
    for signal in latest_signals:
        if trade_alert:= get_alert_details(signal):
            trade_alerts.append(trade_alert)
    if not trade_alerts:
        trade_alerts.append(test_alert)

    for alert in trade_alerts:
        send_alert(alert_details=alert)




