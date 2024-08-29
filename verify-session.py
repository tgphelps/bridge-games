
import sys


def main() -> None:
    assert len(sys.argv) == 2
    boards: list[int] = []
    with open(sys.argv[1], 'rt') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.rstrip()
            if line == '':
                continue
            assert line.startswith('http')
            n = board_number(line)
            if n in boards:
                print(f'Error: board {n} is duplicated')
                sys.exit(1)
            boards.append(n)
    boards = sorted(boards)
    show_boards(boards)


def board_number(line: str) -> int:
    fld = line.split('&')
    for f in fld:
        if f.startswith('b='):
            f2 = f.split('=')
            return int(f2[1])
    assert False


def show_boards(b: list[int]) -> None:
    print(b)


if __name__ == '__main__':
    main()
