
# This program updates the database by adding the auction, result,
# and opening lead for given boards.
#
# usage: add-info.py <session>

import sqlite3
import sys


DB = 'deals.db'


class Globals:
    session: str


g = Globals()
g.session = ''


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: add-info.py <session>', file=sys.stderr)
        sys.exit(2)
    g.session = sys.argv[1]

    board = 0
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute('begin transaction')
    while True:
        ans = input('Board (q to quit)? >')
        if ans == 'q':
            break
        if ans == '':
            board += 1
        else:
            try:
                board = int(ans)
            except ValueError:
                print('Invalid board. Exiting.')
                break
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
    "Ask user for result and opening lead of this board."
    print('Adding info for board', board)
    result = 0
    auction = input('Auction? >')
    try:
        result = int(input('Result? >'))
    except ValueError:
        print('ERROR: result is not an integer.')
    lead = input('Opening lead? >')

    return result, auction, lead


def update_db(board: int, cur: sqlite3.Cursor,
              result: int, auction: str, lead: str) -> None:
    "UPDATE the board in the database."
    # Note that opening_lead will be '', not NONE, if it was not given.
    print(f'update result={result} a={auction} l={lead}')
    stmt = '''update deals
              set result = ?, auction = ?, opening_lead = ?
              where session = ? and board = ?'''
    cur.execute(stmt, (result, auction, lead, g.session, board))


if __name__ == '__main__':
    main()
