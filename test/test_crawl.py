import unittest
from unittest import mock

from pyphpbb import Crawler


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.dispatcher = mock.Mock()
        self.fetcher = mock.Mock()
        self.crawler = Crawler(self.dispatcher, self.fetcher)

    def test_crawler_wont_dispach_seen_urls(self):
        self.crawler.seen.add('foo.com')
        self.crawler.crawl_thread('foo.com')
        self.assertEqual(self.dispatcher.call_count, 0)

    def test_dispatched_url_added_to_seen(self):
        self.crawler.crawl_thread('foo.com')
        self.assertEqual(
            {'foo.com'},
            self.crawler.seen)

    def test_job_added_to_dispatcher(self):
        self.crawler.crawl_thread('foo.com')
        self.dispatcher.put.assert_called_once_with(
            'foo.com', self.crawler.extract_thread)

    def test_extract_thread(self):
        extractor = mock.MagicMock()
        extractor.from_response.return_value = extractor
        self.crawler.EXTRACTOR = extractor
        response = mock.Mock()
        self.crawler.extract_thread(response)
        extractor.from_response.assert_called_once_with(response)
        self.assertEqual(extractor.extract_thread_links.call_count, 1)
        self.assertEqual(extractor.extract_posts.call_count, 1)


if __name__ == "__main__":
    unittest.main()
