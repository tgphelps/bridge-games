
def _parse_contract(auction: str) -> list[str]:
    a_list: list[str] = []
    assert auction.endswith('ppp')
    just_saw_num = False
    for c in auction:
        if not just_saw_num:
            if c in 'pxr':
                a_list.append(c)
            elif c in '1234567':
                num = c
                just_saw_num = True
            else:
                assert 'Bad character in auction' == ''
        else:  # should see a suit now
            if c in 'shdcn':
                a_list.append(num + c)
                just_saw_num = False
            else:
                assert 'Bad suit in auction' == ''
    return a_list


def _find_last_bid(auction: list[str]) -> str:
    # XXX fix this double reverse
    modifier = ''
    for call in reversed(auction):
        # print('checking call:', call)
        if call == 'r':
            modifier = 'XX'
            # print('modifier:', modifier)
        elif call == 'x' and modifier == '':
            modifier = 'X'
            # print('modifier:', modifier)
        elif call not in 'px':
            # print('call =', call)
            return call + modifier
    assert False


_bid_order = {
    'n': 'nesw',
    'e': 'eswn',
    's': 'swne',
    'w': 'wnes'
}


def _who_was_bidder(dealer: str, n: int) -> str:
    'Return who bid at index n in the auction.'
    n = n % 4
    return _bid_order[dealer][n]


def get_contract(dealer: str, auction: str) -> tuple[str, str]:
    'Return contract and declarer, using dealer and auction.'

    # Returns dealer and 'pass' if passed out.

    if auction == 'pppp':
        return dealer.upper(), 'PASS'

    auc = _parse_contract(auction)
    bid = _find_last_bid(auc)
    # print('auc:', auc, 'bid:', bid)
    suit = bid[1]
    index_of_bid = auc.index(bid[0:2])
    # print('contract at index:', index_of_bid)
    first_index = index_of_bid % 2  # either 0 or 1
    first_bidder = -1
    for n in range(first_index, len(auc), 2):
        # print('check index:', n, auc[n], auc)
        if len(auc[n]) == 2 and auc[n][1] == suit:
            # print('first bid at:', n)
            first_bidder = n
            break
        else:
            # print('no')
            pass
    # print(f'who was bidder {first_bidder} with dealer {dealer}')
    return bid.upper(), _who_was_bidder(dealer, first_bidder).upper()
