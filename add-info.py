
import sqlite3
import sys


DB = 'deals.db'


class Globals:
    session: str


g = Globals()
g.session = ''


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: add-info.py <session_id>', file=sys.stderr)
        sys.exit(2)
    g.session = sys.argv[1]

    board = 0
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute('begin transaction')
    while True:
        ans = input('Board? >')
        if ans == '':
            break
        if ans == 'n':
            board += 1
        else:
            board = int(ans)
        update_board(board, cur)
        print()
    cur.close()
    db.commit()
    db.close()


def update_board(n: int, cur: sqlite3.Cursor) -> None:
    "Update result, auction, and opening lead for board n."
    result, auction, lead = read_additional_info(n)
    update_db(n, cur, result, auction, lead)


def read_additional_info(board: int) -> tuple[int, str, str]:
    print('Adding info for board', board)
    result = int(input('Result? >'))
    auction = input('Auction? >')
    lead = input('Opening lead? >')
    return result, auction, lead


def update_db(board: int, cur: sqlite3.Cursor,
              result: int, auction: str, lead: str) -> None:
    print(f'update result={result} a={auction} l={lead}')
    stmt = '''update deals
              set result = ?, auction = ?, opening_lead = ?
              where session_id = ? and deal_id = ?'''
    cur.execute(stmt, (result, auction, lead, g.session, board))


if __name__ == '__main__':
    main()
