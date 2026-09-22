import traceback
from mooneazy.trading.results import get_signal_results
from .appwrite_api.signals_table import SignalsTable 
from .appwrite_api.messages import send_push_notifications


def main(context):
    signal_id = context.req.query.get('id')
    if not signal_id:
        return context.res.text('Missing Signal ID', status_code=400)

    try:
        table = SignalsTable()
        signal = table.get_signald(signal_id=signal_id)
        if signa['data']['status'] == 'closed':
            return context.res.json(signal)

        sginal_result = get_signal_results(signal)
        if not signal_reults:
            return context.res.json(signal)
        table.update_signal(signal)
    except Exception as e:
        errors = traceback.format_exc()
        context.log(errors)
        results['errors'] = errors
    return context.res.json(results)


