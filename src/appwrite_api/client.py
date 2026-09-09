import os
from appwrite.client import Client


def get_client():
    client = Client()
    ENDPOINT = os.environ.get("APPWRITE_FUNCTION_API_ENDPOINT", None)
    PROJECT_ID = os.environ.get("APPWRITE_FUNCTION_PROJECT_ID", None)
    API_KEY = os.environ.get("APPWRITE_FUNCTION_API_KEY", None)
    if not ENPOINT:
        raise ValueError('Missing ENPOINT')
    if not PROJECT_ID:
        raise ValueError("Missing PROJECT_ID")
    if not API_KEY:
        raise ValueError("Missing API_KEY")

    client.set_endpoint(ENPOINT)
    client.set_project(PROJECT_ID)
    client.set_key(API_KEY(API_KEY)
    return client

