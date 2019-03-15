import os.path
import unittest

from lxml.html import fromstring

from pyphpbb import PHPBB2Extractor
from pyphpbb.types import Post


class TestPHPBBExtractor(unittest.TestCase):

    def setUp(self):
        fixture = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'test',
            'fixtures',
            'test.html')
        with open(fixture) as fh:
            self.extractor = PHPBB2Extractor(fromstring(fh.read()))

    def test_extract_thread_links(self):
        self.assertEqual(
            {'next', 'prev'},
            self.extractor.extract_thread_links())

    def test_extract_posts(self):
        expected_posts = [
            Post("137700", 'rcx822', '2016-01-01T09:00:00', 'Post body 1 with an image  -- foobar.gif'),
            Post("137707", 'ukdave2002', '2016-01-01T12:12:00', '\\nPost body 2 -- ')]
        self.assertEqual(
            self.extractor.extract_posts(),
            expected_posts)



if __name__ == "__main__":
    unittest.main()
