import traceback
from mooneazy.trading.results import get_new_results
from .appwrite_api.signals_table import SignalsTable
from .appwrite_api.messages import send_push_notifications

TEST_SIGNAL_ID = '6ab244cc00375e76cf65'


def main(context):
    cors_headers = {
        'Access-Control-Allow-Origin': '*, localhost:8081',  # Allows localhost:8081, mobile simulators, and devices
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-appwrite-project, x-appwrite-jwt, x-sdk-version',
        'Access-Control-Max-Age': '86400'    # Cache preflight response for 24 hours
    }

    # 2. Handle the browser preflight OPTIONS request
    if context.req.method == 'OPTIONS':
        return context.res.text('', 200, cors_headers)
    
    signal_id = context.req.query.get('id')
    table = SignalsTable()

    limit = context.req.query.get('latest')
    if limit:
        latest_signals = table.get_latest_signals(int(limit))
        return context.res.json(latest_signals, 200, cors_headers)

    pending_signals = []
    results = []
    errors = []
    
    try:
        if not signal_id:
            pending_signals = table.get_pending_signals()
        else:
            pending_signals.append(
                table.get_pending_signal(signal_id=signal_id)
            )
        results = get_new_results(pending_signals)
        table.update_signals(results)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
        return context.res.json(errors)
    return context.res.json(results, 200, cors_headers)



