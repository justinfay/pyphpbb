import csv
from urllib.parse import urlparse


def fqdn(url):
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Malformed url: {}".format(url))
    return parsed.netloc


def write_csv(fh, posts):
    """
    Utility function for writing CSV file.
    """
    writer = csv.writer(fh, delimiter=',')
    writer.writerows(posts)
