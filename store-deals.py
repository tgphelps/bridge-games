"""
store-deals.py: Store contents of a hand viewer file in the database.

Usage:
    store-deals.py [ -v ] -s <session> HAND_FILE
    store-deals.py --version
    store-deals.py --help

Options:
    -s <session>        Session-id to use for these hands.
    --verbose, -v       Be talkative for debugging.
    --version           Show version and exit.
    -h --help           Show this message and exit.
"""

import sqlite3
# from typing import TextIO
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
    fname = args['HAND_FILE']
    session = args['-s']
    store_deals(fname, session)


def store_deals(fname: str, session: str) -> None:
    "Read URLs from file and insert into database."
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute('begin transaction')
    with open(fname, 'rt') as f:
        for line in f.readlines():
            line = line.rstrip()
            if line == '':
                continue
            assert line.startswith('http:')
            b = board_number(line)
            insert_row(session, b, line, cur)
    cur.close()
    db.commit()
    db.close()


def insert_row(session: str, n: int, line: str, cur: sqlite3.Cursor):
    "Insert one deal into the database."
    print(line)
    print(f'insert session {session} board {n}')
    stmt = '''insert into Deals
              (session, board, viewer_link)
              values (?, ?, ?)'''
    cur.execute(stmt, (session, n, line))


def board_number(line: str) -> int:
    "Find board number in URL."
    fld = line.split('&')
    for f in fld:
        if f.startswith('b='):
            f2 = f.split('=')
            return int(f2[1])
    assert False


if __name__ == '__main__':
    main()
