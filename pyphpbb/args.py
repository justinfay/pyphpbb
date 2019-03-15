"""
Argument parsing for pyphpbb.
"""

import argparse


THREAD_HELP = "One or more treads to scrape."
RATELIMIT_HELP = "A time limit for dispatching requests to any single host."
OUTFILE_HELP = "A file for writing scraped posts too, defaults to STDOUT"
VERBOSE_HELP = "Print a summary of HTTP requests."


parser = argparse.ArgumentParser(description='PHPBB scraper')
parser.add_argument(
    '--threads', '-t',
    nargs="+", action='store', help=THREAD_HELP, required=True)
parser.add_argument(
    '--ratelimit', '-r',
    action="store", default=5, type=int, help=RATELIMIT_HELP)
parser.add_argument(
    '--outfile', '-o', action="store", help=OUTFILE_HELP)
parser.add_argument(
    '--verbose', '-v', action="store_true", help=VERBOSE_HELP)


def parse_args():
    """
    Parse the supplied args and return a namespace.
    """
    return parser.parse_args()


if __name__ == "__main__":
    print(parse_args())
