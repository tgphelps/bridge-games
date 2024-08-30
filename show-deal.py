
"""
show-deal.py: Store contents of a hand viewer file in the database.

Usage:
    show-deal.py [ -t ] -s <session>
    show-deal.py --version
    show-deal.py --help

Options:
    -s <session>        Session-id to use for these hands.
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
    g.session = args['-s']
    if args['--testing']:
        g.testing = True
    print(args)

    board = 0
    while True:
        ans = input('Board? >')
        if ans == '':
            break
        if ans == 'n':
            board += 1
        else:
            board = int(ans)
        show_board(board)


def show_board(board: int) -> None:
    url = ''
    result = 0
    auction = ''
    lead = ''
    db = sqlite3.connect(DB)
    cur = db.cursor()
    stmt = '''select viewer_link, result, auction, opening_lead from Deals
    where session_id = ? and deal_id = ?'''
    cur.execute(stmt, (g.session, board))
    for row in cur:
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
    db.close()


def edit_link(link: str) -> str:
    p = re.compile('{.*}')
    m = p.search(link)
    assert m is not None
    r = m.span()
    return link[0:r[0]] + link[r[1]:]


def insert_auction_and_comments(url: str, auction: str,
                                result: int, lead: str) -> str:
    n = url.find('&a=')
    assert n > 0
    first = url[0: n+3]
    rem = url[n+3:]
    n = rem.find('&')
    assert n >= 0
    last = rem[n:]
    if g.testing:
        auction = insert_comments(auction, result, lead)
        last = last.replace('%20', ' ', -1)
    print('first:', first)
    print('auction:', auction)
    print('last:', last)
    url2 = first + auction + last
    return url2


def insert_comments(auction: str, result: int, lead: str) -> str:
    # XXX
    # return s[0:9] + '{test}' + s[9:]
    # return f'{{result = {result},  opening lead = {lead}}}' + auction
    return auction + f'{{result = {result},  opening lead = {lead}}}'
    # return auction + '{test}' OKAY


if __name__ == '__main__':
    main()
