
import re
import sqlite3
import sys
import webbrowser


DB = 'deals.db'


class Globals:
    session: str


g = Globals()
g.session = ''


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: show-deals.py <session_id>', file=sys.stderr)
        sys.exit(2)
    g.session = sys.argv[1]

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
        if auction != '':
            url2 = insert_good_auction(url2, auction)
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


def insert_good_auction(url: str, auction: str) -> str:
    n = url.find('&a=')
    assert n > 0
    first = url[0: n+3]
    rem = url[n+3:]
    n = rem.find('&')
    assert n >= 0
    last = rem[n:]
    url2 = first + auction + last
    # print('fixed:', url2)
    return url2


if __name__ == '__main__':
    main()
