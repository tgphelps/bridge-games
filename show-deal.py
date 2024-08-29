
import re
import sqlite3
import webbrowser


DB = 'deals.db'
SESSION = 'acbl'


def main() -> None:
    while True:
        ans = input('Board? >')
        if ans == '':
            break
        board = int(ans)
        show_board(board)


def show_board(board: int) -> None:
    db = sqlite3.connect(DB)
    cur = db.cursor()
    s = '''select viewer_link from Deals
    where session_id = ? and deal_id = ?'''
    cur.execute(s, (SESSION, board))
    for row in cur:
        link = row[0]
        # link = link.replace('%', '$', -1)
        # link2 = html.escape(link)
        link2 = edit(link)
        print(link2)
        # assert link == link2
        webbrowser.open(link2)
    db.close()


def edit(link: str) -> str:
    p = re.compile('{.*}')
    m = p.search(link)
    assert m is not None
    r = m.span()
    return link[0:r[0]] + link[r[1]:]


if __name__ == '__main__':
    main()
