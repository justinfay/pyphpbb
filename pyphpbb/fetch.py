from http import client

import requests
from requests.exceptions import RequestException

from .types import FetchResult


class Fetcher:
    """
    The `Fetcher` is responsible for all HTTP
    requests.
    """

    def __init__(self):
        # Log of requests made.
        self.requests = []

    def fetch(self, url):
        """
        Fetch a url and return a response.
        """

        try:
            response = requests.get(url)
        except RequestException as exc:
            result = FetchResult(
                url, None, None, exc.__class__.__name__)
        else:
            result = FetchResult(
                response.url,
                response.status_code,
                response.elapsed,
                None)
        finally:
            self.requests.append(result)

        if result.exception is None and response.status_code == client.OK:
            return response
        return None

    def work(self, dispatcher):
        """
        Listen to a dispatcher for jobs and perform them.
        """
        url, extractor = dispatcher.get()
        response = self.fetch(url)
        if response:
            extractor(response)
