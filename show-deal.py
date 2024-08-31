
"""
show-deal.py: Store contents of a hand viewer file in the database.

Usage:
    show-deal.py [ -t ] SESSION
    show-deal.py --version
    show-deal.py --help

SESSION is the 'session' in the database to query

Options:
    --testing, -t       Use for testing code.
    --version           Show version and exit.
    -h --help           Show this message and exit.
"""

import re
import sqlite3
import webbrowser
import docopt  # type: ignore


DB = 'deals.db'
VERSION = '0.00'


class Globals:
    testing: bool
    session: str


g = Globals()
g.testing = False
g.session = ''


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    g.session = args['SESSION']
    if args['--testing']:
        g.testing = True
    # print(args)

    db = sqlite3.connect(DB)
    cur = db.cursor()
    board = 0
    while True:
        ans = input('Board? >')
        if ans == 'q':
            break
        if ans in ('', 'n'):
            board += 1
        else:
            board = int(ans)
        show_board(board, cur)
    cur.close()
    db.close()


def show_board(board: int, cur: sqlite3.Cursor) -> None:
    "Display the board in BBO."
    url = ''
    result = 0
    auction = ''
    lead = ''

    stmt = '''select viewer_link, result, auction, opening_lead from Deals
    where session = ? and board = ?'''
    cur.execute(stmt, (g.session, board))
    rows_found = 0
    for row in cur:
        rows_found += 1
        url, result, auction, lead = row
        url2 = edit_link(url)
        if auction:  # auction will be None if not added
            url2 = insert_auction_and_comments(url2, auction, result, lead)
        # print(link2)
        if lead != '':
            print('Opening lead:', lead)
        if result != 0:
            print('Result:', result)
        webbrowser.open(url2)
    if rows_found == 0:
        print(f'Board {board} is not available.')


def edit_link(link: str) -> str:
    p = re.compile('{.*}')
    m = p.search(link)
    assert m is not None
    r = m.span()
    return link[0:r[0]] + link[r[1]:]


def insert_auction_and_comments(url: str, auction: str,
                                result: int, lead: str) -> str:
    "Insert auction, result, and opening lead into the URL."
    n = url.find('&a=')
    assert n > 0
    first = url[0: n+3]
    rem = url[n+3:]
    n = rem.find('&')
    assert n >= 0
    last = rem[n:]
    # if g.testing:
    auction = insert_comments(auction, result, lead)
    last = last.replace('%20', ' ', -1)
    # print('first:', first)
    # print('auction:', auction)
    # print('last:', last)
    url2 = first + auction + last
    return url2


def insert_comments(auction: str, result: int, lead: str) -> str:
    "Insert result and opening lead into auction."
    # return auction + f'{{result = {result},  opening lead = {lead}}}'
    if result > 0:
        s1 = f'Made {result}.   '
    else:
        s1 = f'Down {-result} '
    s2 = 'Opening lead: ' + lead
    return auction + '{' 'Result: ' + s1 + s2 + '}'


if __name__ == '__main__':
    main()
