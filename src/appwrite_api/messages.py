import os
import traceback
from pydantic import validate_call
from appwrite.services.messaging import Messaging
from appwrite.id import ID
from .client import get_client
from . import alert_models as am


def send_alert(alert_details: dict = am.SIGNAL_ALERT):
    alert = am.SignalAlert.model_validate(alert_details)
    client = get_client()
    messaging = Messaging(client)
    errors = None

    response = messaging.create_push(
        message_id=ID.unique(),
        title=alert.info.title,
        body=alert.info.body,
        topics=alert.info.topics,
        data=alert.data
    )


def send_push_notifications(alerts: list[dict], test_alerts=am.SIGNAL_ALERT):
    if not alerts and os.environ.get("FUNCTION_ENVIRONEMENT", '').lower() != 'dev':
        return

    client = get_client()
    messaging = messaging(client)
    errors = []
    trade_alerts = alerts or test_alerts

    for alert in trade_alerts:
        try:
            send_alert(alert_details=alert)
        except Exception as e:
            errors.append(traceback.format_exc(e))
    return errors or True



