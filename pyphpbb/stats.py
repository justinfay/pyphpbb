from collections import defaultdict
from datetime import timedelta
import sys


def report(fetches, posts, fh=sys.stdout):
    """
    Print a summary of all HTTP requests.
    """
    print("Summary\n", file=fh)

    # How many posts were scraped:
    print('Scraped: {0} forum posts'.format(len(posts)))

    # How many total requests made.
    print("Performed: {0} HTTP requests".format(len(fetches)), file=fh)

    # Average request time.
    request_time_avg = (
        sum((fetch.time for fetch in fetches), timedelta(0)) /
        len(fetches))
    print('Average request time: {0}'.format(request_time_avg, file=fh))

    # Breakdown of return codes.
    return_codes = defaultdict(int)
    exceptions = defaultdict(int)
    for fetch in fetches:
        return_codes[fetch.status] += 1
    print('Return codes', file=fh)
    for (code, count) in sorted(return_codes.items()):
        print("    {0}: {1}".format(code, count), file=fh)

    # Breakdown of exceptions.
    exceptions = defaultdict(int)
    for fetches in fetches:
        if fetch.exception:
            exceptions[fetch.exception] += 1
    for exception, count in sorted(return_codes.items()):
        print("    {0}: {1}".format(exception, count), file=fh)
