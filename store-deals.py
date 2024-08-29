"""
store-deals.py: Store contents of a PBN file in the database.

Usage:
    store-deals.py [ -v ] -s <session> HAND_FILE
    store-deals.py --version
    store-deals.py --help

Options:
    -s                  Session-id to use for these hands.
    --verbose, -v       Be talkative for debugging.
    --version           Show version and exit.
    -h --help           Show this message and exit.
"""

import sqlite3
from typing import TextIO
import docopt  # type: ignore


VERSION = '0.00'
DB = 'deals.db'


class Globals:
    verbose: bool


g = Globals
g.verbose = False


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    if args['--verbose']:
        g.verbose = True
        print(args)


if __name__ == '__main__':
    main()
