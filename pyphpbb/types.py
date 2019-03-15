from collections import namedtuple


FetchResult = namedtuple('FetchResult', 'url status time exception')
Post = namedtuple('Post', 'id name date body')

