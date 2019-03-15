from http import client
import unittest

from requests.exceptions import HTTPError
import responses

from pyphpbb import Fetcher


class TestFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = Fetcher()

    @responses.activate
    def test_fetch_not_ok(self):
        responses.add(
            responses.GET,
            'http://foo.com/',
            status=client.INTERNAL_SERVER_ERROR)
        self.fetcher.fetch('http://foo.com/')
        # Cant find an easy way to mock elapsed time.
        actual = self.fetcher.requests.pop()
        actual = actual._replace(time=None)
        self.assertEqual(
            actual,
            ('http://foo.com/', 500, None, None))

    @responses.activate
    def test_fetch_raises_captures_exception(self):
        responses.add(responses.GET, 'http://foo.com/', body=HTTPError())
        self.assertIsNone(self.fetcher.fetch('http://foo.com/'))
        self.assertEqual(
            self.fetcher.requests.pop(),
            ('http://foo.com/', None, None, 'HTTPError'))

    @responses.activate
    def test_fetch_200(self):
        responses.add(responses.GET, 'http://foo.com/', status=client.OK)
        self.fetcher.fetch('http://foo.com/')
        actual = self.fetcher.requests.pop()
        actual = actual._replace(time=None)
        self.assertEqual(
            actual,
            ('http://foo.com/', 200, None, None))


if __name__ == "__main__":
    unittest.main()
