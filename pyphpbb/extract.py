from dateutil.parser import parse
from itertools import chain
from lxml.html import fromstring, HTMLParser

from .types import Post


class PHPBB2Extractor:
    """
    PHPBB2 specific extraction routines.
    """

    def __init__(self, tree):
        self.tree = tree

    @classmethod
    def from_response(cls, response):
        """
        Alternative constructor which parses a a HTTP response
        into an lxml instance body.
        """
        # Create a new parser to enable threading release GIL.
        parser = HTMLParser()
        tree = fromstring(
            response.content, parser=parser, base_url=response.url)
        tree.make_links_absolute()
        return cls(tree)

    def extract_thread_links(self):
        """
        Extract Next/Previous links from a thread.
        """
        prev = self.tree.xpath("//a[text()='Previous']/@href")
        next_ = self.tree.xpath("//a[text()='Next']/@href")
        return set(prev + next_)

    def extract_posts(self):
        """
        Extract posts from a thread page.
        """
        posts = self.tree.xpath("//tr[./td/span[@class='name']]")
        return [
            self._extract_post(post)
            for post in posts]

    def _extract_post(self, tree):
        return Post(
            self._extract_id(tree),
            self._extract_username(tree),
            self._extract_date(tree),
            self._extract_body(tree))

    def _extract_id(self, tree):
        try:
            return tree.xpath(".//span[@class='name']/a")[0].attrib['name']
        except (KeyError, IndexError):
            return None

    def _extract_username(self, tree):
        try:
            return tree.xpath(".//span[@class='name']/b/text()")[0]
        except IndexError:
            return None

    def _extract_body(self, tree):
        try:
            # Quotes mess up post structure so there may be
            # multiple spans containing text and images.
            post_bodies = tree.xpath(".//span[@class='postbody']")
        except IndexError:
            return None

        text = self._extract_content(post_bodies)
        images = self._extract_images(post_bodies)
        return text + ' -- ' + images

    def _extract_content(self, trees):
        text = ''.join(
            ''.join(tree.xpath(".//text()")).encode('unicode-escape').decode()
            for tree in trees)
        # Remove signature if present.
        return text.rsplit('_________________', 1)[0]

    def _extract_images(self, trees):
        images = chain.from_iterable(tree.xpath(".//@src") for tree in trees)
        return ' '.join(
            image
            for image in images
            if not image.startswith("images/smiles/"))

    def _extract_date(self, tree):
        try:
            posted = tree.xpath(
                ".//span[@class='postdetails']")[1].xpath('.//text()')[0]
        except (IndexError, AttributeError):
            return None
        try:
            posted = parse(posted.replace('Posted: ', ''))
        except ValueError:
            return None
        return posted.isoformat()
