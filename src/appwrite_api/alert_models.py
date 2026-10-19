from pydantic import BaseModel

class AlertInfo(BaseModel):
    title: str
    body: str
    topics: list[dict]


class AlertData(BaseModel):
    path: str
    symbol: str
    utc_time: str
    signal_type: str
    id: str | None = None


class ResultsData(BaseModel):
    path: str
    symbol: str
    utc_time: str
    signal_type: str
    id: str


class ResultsAlert(BaseModel):
    info: AlertInfo
    data: ResultsData


class SignalAlert(BaseModel):
    title: str
    body: str 
    topics: list
    data: AlertData


ALERT_INFO = {
    'title': 'sample title',
    'body': 'sample alert body!!',
    'topics': ['mooneazy_signals'],
}


RESULTS_DATA = {
    'signal_type': 'signal_type',
    'path': '/',
    'utc_time': 'utc sample time',
    'signal_id': 'uuid23245343'
}


SIGNAL_DATA = {
    'signal_type': 'signal_type',
    'path': '/',
    'utc_time': 'utc sample time'
 
}


SIGNAL_ALERT = [
    {
        'title': 'sample title',
        'body': 'sample alert body!!',
        'topics': ['mooneazy_signals'],
        'data': {
            'signal_type': 'signal_type',
            'path': '/',
            'utc_time': 'utc sample time',
            'id': 'uuid23245343'
        }
    }
]


RESULTS_ALERT = {
    'info': ALERT_INFO, 
    'data': RESULTS_DATA

}


