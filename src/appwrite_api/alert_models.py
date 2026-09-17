from typing import TypedDict,
from pydantic import BaseModel

class AlertInfo(BaseModel):
    title: str
    body: str
    topics: list[dict]


class SignalData(BaseModel):
    path: str
    symbol: str
    utc_time: str
    signal_type: str


class ResultsData(BaseModel):
    path: str
    symbol: str
    utc_time: str
    signal_type: str
    signal_id: str


class ResultsAlert(BaseModel):
    info: AlertInfo
    data: ResultsData


class SignalAlert(BaseModel):
    info: AlertInfo
    data: SignalData


ALERT_INFO = {
    'title': 'sample title',
    'body': 'sample alert body!!',
    'topics': 'mooneazy_signals',
}


RESULTS_DATA = {
    'signal_type': 'signal_type',
    'path': '/',
    'utc_time': 'utc sample time'
    'signal_id': 'uuid23245343'
}


SIGNAL_DATA = {
    'signal_type': 'signal_type',
    'path': '/',
    'utc_time': 'utc sample time'
 
}


SIGNAL_ALERT = {
    'info': ALERT_INFO, 
    'data': SIGNAL_DATA
}


RESULTS_ALERT = {
    'info': ALERT_INFO, 
    'data': RESULTS_DATA

}


