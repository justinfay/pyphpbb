import time

from .util import fqdn


class DispatcherEmpty(Exception):
    """
    Exception raised when a task is requested
    from an empty dispatcher.
    """


class Dispatcher:
    """
    The dispatcher holds all jobs waiting to be dispatched
    and manages rate limiting tasks on a hostname basis.
    """

    def __init__(self, rate_limit=None):
        # Time limit in seconds for subsequent requests
        # to the same host.
        self.rate_limit = rate_limit
        # Mapping of hostname to last dispatched task.
        self._history = {}
        self._queue = []

    def put(self, url, extractor):
        """
        Schedule a task to be dispatched.
        """
        self._queue.append((url, extractor))

    def get(self):
        """
        Get and return the next task to be processed.
        """
        while True:
            try:
                url, extractor = self._queue.pop(0)
            except IndexError:
                raise DispatcherEmpty()

            if self._is_limited(url):
                self._queue.append((url, extractor))
                time.sleep(1)
                continue

            break

        if self.rate_limit is not None:
            self._history[fqdn(url)] = time.time()

        return (url, extractor)

    def _is_limited(self, url):
        """
        Is this url rate limited.
        """
        if self.rate_limit is None:
            return False

        now = time.time()
        url = fqdn(url)
        last = self._history.get(url, 0)
        elapsed = now - last

        return elapsed <= self.rate_limit
