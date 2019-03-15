from .extract import PHPBB2Extractor
from .dispatch import DispatcherEmpty


class Crawler:
    """
    The `Crawler` contains the business logic for
    scraping a forum.

    It schedules tasks with the dispatcher and
    contains the entry points for the extraction
    tasks (which it delegates to a forum specific
    `Extractor`.
    """

    EXTRACTOR = PHPBB2Extractor

    def __init__(self, dispatcher, fetcher, thread_urls=()):
        self.dispatcher = dispatcher
        self.fetcher = fetcher
        self.thread_urls = thread_urls
        self.posts = []
        self.seen = set()

    def crawl(self):
        """
        Entry point for performing the actual crawling
        of forums.
        """
        self.crawl_threads()
        while True:
            try:
                self.fetcher.work(self.dispatcher)
            except DispatcherEmpty:
                break

    def crawl_threads(self):
        """
        Crawl all threads specified by the user.
        """
        for thread_url in self.thread_urls:
            self.crawl_thread(thread_url)

    def crawl_thread(self, thread_url):
        """
        Crawl a given thread.
        """
        if thread_url not in self.seen:
            self.dispatcher.put(thread_url, self.extract_thread)
            self.seen.add(thread_url)

    def extract_thread(self, response):
        """
        Extract posts and thread links from a HTTP
        response. Note the actual extraction process
        is delegated to a dedicated forum extractor.
        """
        extractor = self.get_extractor(response)

        for thread_page_url in extractor.extract_thread_links():
            self.crawl_thread(thread_page_url)
        for post in extractor.extract_posts():
            self.posts.append(post)

    def get_extractor(self, response):
        """
        Return an extractor instance for the given responce.
        """
        return self.EXTRACTOR.from_response(response)
