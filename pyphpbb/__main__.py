import sys

from .args import parse_args
from .crawl import Crawler
from .dispatch import Dispatcher
from .fetch import Fetcher
from .util import write_csv
from .stats import report


def runner(args):

    dispatcher = Dispatcher(args.ratelimit)
    fetcher = Fetcher()
    crawler = Crawler(dispatcher, fetcher, thread_urls=args.threads)

    try:
        crawler.crawl()
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        if args.outfile is None:
            write_csv(sys.stdout, crawler.posts)
        else:
            with open(args.outfile, 'w') as fh:
                write_csv(fh, crawler.posts)
        if args.verbose:
            report(fetcher.requests, crawler.posts)


def main():
    args = parse_args()
    runner(args)


if __name__ == "__main__":
    main()
