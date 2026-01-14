from ..transport.http import HTTPClient

class BaseEndpoint:
    def __init__(self, client: HTTPClient):
        self.client = client
