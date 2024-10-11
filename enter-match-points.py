
import sys
from typing import TextIO


# Enter match points for each hand in a session.
# Usage:
#    ./enter-match-points.py <output-file>


def main() -> None:
    if len(sys.argv) != 2:
        print('usage: ./enter-match-points.py <output-file>',
              file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'wt') as f:
        session, max_match_points = get_session_and_max_points()
        print('session:', session, file=f)
        print('max_match_points:', max_match_points, file=f)
        print('Enter q to quit.')
        write_board_data(f)


def get_session_and_max_points() -> tuple[str, str]:
    session = input('Session: >')
    max_points = input('Max match points: >')
    return session, max_points


def write_board_data(f: TextIO):
    n = 1
    while True:
        val = input(f'Board {n}: >')
        if val.startswith('q'):
            break
        if val != '':
            print('board:', n, val, file=f)
        n += 1


if __name__ == '__main__':
    main()
