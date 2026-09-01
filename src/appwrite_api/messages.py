from appwrite.services.messaging import Messaging
from appwrite.id import ID
from .client import get_client

test_signals = [
    {
        "symbol": "btc",
        "utc_time": "test_utc_time",
        "signal_type": "SFP_BUY"
    }

]

def send_push_notifications(signals, test_signals=test_signals):
    client = get_client() 
    messaging = Messaging(client)
    errors = []
    trade_signals = signals or test_signals
    for signal in trade_signals:
        try:
            symbol = signal['symbol']
            message_body = f"{signal['signal_type']} on {signal['utc_time']}"
            response = messaging.create_push(
                message_id=ID.unique(),
                title=f"{symbol} TRADE ALERT!!",
                body= message_body,
                topics=['mooneazy_signals'],
                data = {
                    'path': '/signals'
                }
            )

        except Exception as e:
            errors.append(f" FAILED TO SEND PUSH NOTIFICATION FOR {signal}!! \n {e}")
    return errors or True


