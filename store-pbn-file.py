
"""
store-pbn-file.py: Store contents of a PBN file in the database.

Usage:
    store-pbn-file.py [ -v ] -s <session> PBN_FILE [ HANDS ]
    store-pbn-file.py --version
    store-pbn-file.py --help

HANDS should be a range of integers (e.g., 1-24)
Options:
    -s                  Session-id to use for these hands.
    --verbose, -v       Be talkative for debugging.
    --version           Show version and exit.
    -h --help           Show this message and exit.
"""

import sqlite3
from typing import TextIO
import docopt  # type: ignore


VERSION = '0.00'
DB = 'deals.db'


class Globals:
    verbose: bool


g = Globals
g.verbose = False


class Deal:
    session_id: str
    deal_id: str
    name_north: str
    name_south: str
    name_east: str
    name_west: str
    dealer: str
    vuln: str
    hand_north: str
    hand_south: str
    hand_east: str
    hand_west: str
    auction: str
    contract: str
    opening_lead: str


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    if args['--verbose']:
        g.verbose = True
        print(args)

    hand_start = 1
    hand_end = 99
    session_id = args['-s']
    if args['HANDS']:
        s = args['HANDS']
        assert '-' in s
        fld = s.split('-')
        hand_start = int(fld[0])
        hand_end = int(fld[1])

    pbn_file = args['PBN_FILE']
    store_pbn_file(pbn_file, session_id, hand_start, hand_end)


def store_pbn_file(pbn_file: str, session_id: str,
                   hand_start: int, hand_end: int) -> None:
    "Store all deals from PBN file into database."
    if g.verbose:
        print('storing hands', hand_start, 'to', hand_end)
    with open(pbn_file, 'rt') as f:
        if validate_file(f):
            if g.verbose:
                print(f'Storing file {pbn_file}')
        else:
            print('ERROR: invalid file')
            return
        db = sqlite3.connect(DB)

        while True:
            deal_text = read_deal(f)
            # if g.verbose:
            #     print(deal_text)
            if len(deal_text) == 0:
                break
            hand_num = get_board_num(deal_text)
            if hand_start <= hand_num <= hand_end:
                deal = parse_deal(deal_text)
                store_deal(deal, session_id, db)
        db.close()


def read_deal(f: TextIO) -> list[str]:
    "Read one deal from the PBN file."
    if g.verbose:
        print('Read deal...')
    deal: list[str] = []
    while True:
        line = f.readline()
        if len(line) == 0:
            return []
        line = line.rstrip()
        # print('LINE:', len(line), line)
        if len(line) > 0:
            if not line.startswith('%'):
                deal.append(line)
        else:
            break
    return deal


def parse_deal(lines: list[str]) -> Deal:
    "Parse PBN deal lines into a Deal object."
    d = build_pbn_dict(lines)
    if g.verbose:
        print(d)
    _ = build_deal_obj(d)
    return Deal()


def build_pbn_dict(lines: list[str]) -> dict[str, str]:
    d: dict[str, str] = {}
    for line in lines:
        # A line looks like: [keywd "str"]
        # print('line:', line)
        if not (line.startswith('[') and line.endswith(']')):
            continue
        line = line[1:-1]
        fld = line.split(None, 1)
        # print('fld:', fld)
        assert fld[1].startswith('"') and fld[1].endswith('"')
        value = fld[1][1:-1]
        d[fld[0]] = value
    return d


def build_deal_obj(d: dict[str, str]) -> Deal:
    return Deal()


def store_deal(deal: Deal, session_id: str, db: sqlite3.Connection) -> None:
    "Store deal in database."
    if g.verbose:
        print("storing deal in database.")
    pass


def get_board_num(lines: list[str]) -> int:
    "Extract board number from deal text."
    for line in lines:
        if 'Board' in line:
            fld1 = line.split()
            fld2 = fld1[1].split('"')
            num = int(fld2[1])
            if g.verbose:
                print('Board number is', num)
            return num
    assert False


def validate_file(f: TextIO) -> bool:
    line1 = f.readline()
    line2 = f.readline()
    if len(line1) == 0 or len(line2) == 0:
        return False
    if line1.startswith('% PBN 2.1') \
       and line2.startswith('% EXPORT'):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
