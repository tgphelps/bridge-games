
"""
add-match-points.py: Add matchpoint data to the database.

Usage:
    add-match-points.py [ -d ] <input-file>
    add-match-points.py --version
    add-match-points.py --help

<input-file> is the file to read.

Options:
    --dry-run, -d       Don't do update. Show MP total.
    --version           Show version and exit.
    -h --help           Show this message and exit.
"""

# The input file looks like this:
#
# session 2024xxxx
# max_match_points <float>
# board <int> <float>
# board <int> <float>
# ...
#

import sqlite3
import sys
from typing import TextIO
import docopt   # type: ignore


VERSION = '0.01'
DB = 'deals.db'


class Globals:
    dry_run: bool
    session: str
    max_match_points: float
    total_match_points: float
    board_data: list[tuple[int, float]]


g = Globals()
g.session = ''
g.max_match_points = 0.0
g.total_match_points = 0.0
g.board_data = []
g.dry_run = False


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    input_file = args['<input-file>']
    if args['--dry-run']:
        g.dry_run = True
    # print(args)

    read_input_file(input_file)

    if not g.dry_run:
        print('Updating database...')
        db = sqlite3.connect(DB, isolation_level=None)
        cur = db.cursor()
        # cur.execute('begin transaction')
        add_board_data(cur, db)
        cur.close()
        # print('commit')
        # db.commit()
        db.close()


def read_input_file(fname: str) -> None:
    with open(fname, 'rt') as f:
        g.session = read_session(f)
        g.max_match_points = read_max_match_points(f)
        g.board_data = read_board_data(f)
        if g.dry_run:
            print(g.board_data)
            score = g.total_match_points
            max_score = g.max_match_points * len(g.board_data)
            pct = 100 * score / max_score
            print(f'Total matchpoints: {score:.2f}')
            print(f'Percentage: {pct:5.2f}%')


def read_session(f: TextIO) -> str:
    line = f.readline()
    line = line.strip()
    fld = line.split()
    if fld[0] != 'session:' or not fld[1].startswith('202') \
       or len(fld[1]) != 8:
        print(f'ERROR: Bad session line: {line}')
        sys.exit(1)
    return fld[1]


def read_max_match_points(f: TextIO) -> float:
    line = f.readline()
    line = line.strip()
    fld = line.split()
    if fld[0] != 'max_match_points:':
        assert False
    max = 0.0
    try:
        max = float(fld[1])
    except ValueError:
        print(f'ERROR: bad max match points: {fld[1]}', file=sys.stderr)
        sys.exit(1)
    return max


def read_board_data(f: TextIO) -> list[tuple[int, float]]:
    data: list[tuple[int, float]] = []
    for line in f.readlines():
        line = line.strip()
        fld = line.split()
        if len(fld) != 3 or fld[0] != 'board:':
            print('Bad board line:', line, file=sys.stderr)
            sys.exit(1)
        try:
            board = int(fld[1])
            match_points = float(fld[2])
        except ValueError:
            print('Invalid board data:', line, file=sys.stderr)
            sys.exit(1)
        data.append((board, match_points))
        g.total_match_points += match_points
    return data


SQL = '''update deals set max_points = ?,
            match_points = ?
            where session = ? and board = ?
      '''


def add_board_data(cur: sqlite3.Cursor, db: sqlite3.Connection) -> None:
    for row in g.board_data:
        max = g.max_match_points
        board = row[0]
        score = row[1]
        session = g.session
        data = (max, score, session, board)
        print(f'db update {session} {board} {score}')
        result = cur.execute(SQL, data)
        if result.rowcount != 1:
            print('ERROR: SQL update failed:', data)
            sys.exit(1)

if __name__ == '__main__':
    main()
