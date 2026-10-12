"""CS212 — Poker hands (3,5,4,2).
Deciding which poker hand has the highest rank.

the solution is built incrementally: introduce concepts when
needed, define minimal constructs, test early, refactor later.

Refactoring are documented in the function docstrings.
Improve along 4 dimensions: correctness, elegance, richness, efficiency.
"""

import random 
from collections import Counter


def poker(hands):
    """Find the list of hands with the highest rank.
    update 1: replace max with allmax
    update 2: add hand validation
    TODO (low): consider empty iterable edge case
    """
    hands = [hand for hand in hands if validate(hand)]
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    "Like max, but return all arguments with the maximum value."
    # TODO efficiency fix: generator consumed twice
    key = key or (lambda x: x)
    m = max(key(x) for x in iterable)
    return [x for x in iterable if key(x)==m]


def hand_rank(hand):
    "rank a poker hand."
    ranks = card_ranks(hand)

    if straight(ranks) and flush(hand):  # (10 9 8 7 6)
        return (8, max(ranks))
    elif kind(4, ranks):  # (9 9 9 9 7) -> 9
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):  # (10 10 10 7 7)
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):  # (8 7 5 3 2)
        return (5, ranks)
    elif straight(ranks):  # (8 7 6 5 4)
        return (4, max(ranks))
    elif kind(3, ranks):  # (8 7 2 2 2) -> 2
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):  # (8 5 5 2 2) -> (5, 2)
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):  # (8 7 5 2 2) -> 2
        return (1, kind(2, ranks), ranks)
    else:  # (8 7 5 3 2)
        return (0, ranks)


def card_ranks(cards) -> list[int]:
    """Return descending list of integer ranks for a hand of cards.
    update 1: fix ace-low straight edge case.
    """
    ranks_str = '--23456789TJQKA'

    ranks = [ranks_str.index(r) for r, _ in cards]
    ranks = sorted(ranks, reverse=True)

    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks


def straight(ranks) -> bool:
    "Check if the ranks form a straight."

    total = sum(s-e == 1 for s, e in zip(ranks[:-1], ranks[1:]))
    return total == 4


def flush(hand) -> bool:
    "Check if the ranks form a flush."

    return len(set(c[-1] for c in hand)) == 1


def kind(n: int, ranks):
    """Return the first rank that this hand has exactly n (in 1, 2, 3, 4) of.
    Return None if there is no n-of-a-kind in the hand."""
    c = Counter(ranks)
    res = [k for k, v in c.items() if v == n]
    return None if not res else res[0]


def two_pair(ranks) -> tuple[int, ...] | None:
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None.
    e.g. (8 5 5 2 2) -> (5, 2).
    """
    c = Counter(ranks)
    res = tuple(k for k, v in c.items() if v == 2)
    return res if len(res) == 2 else None


def validate(hand) -> bool:
    "Check if the given hand is valid."
    # TODO check lengths of hand/cards before extraction
    suits = set(c[-1] for c in hand)
    ranks = set(c[0] for c in hand)

    is_proper_hand = (
        len(hand) == 5                              # 5 cards in each hand
        and len(set(hand)) == 5                     # each card is unique
        and suits.issubset(set('SHCD'))             # each card in the four suits
        and ranks.issubset(set('23456789TJQKA'))    # each card in the 13 ranks
        and all(len(c) == 2 for c in hand)          # each card is two characters
    )

    return is_proper_hand


def deal(numhands: int, n=5, shuffle_fn=random.shuffle) -> list[list[str]]:
    """Return a list of numhands hands, each with n cards.
    hand limits: numhands * n <= 52, maximum 10 5-card hands.
    shuffle_fn in [random.shuffle, Knuth_shuffle, teacher_shuffle]

    TODO low: validate dealt hands.
    """
    deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
    shuffle_fn(deck) # in-place shuffle
    return [deck[i*n:(i+1)*n] for i in range(numhands)]


def teacher_shuffle(deck) -> None:
    "Norvig highschool teacher's INPLACE shuffling algorithm."
    # TODO why biased?
    n = len(deck)
    swapped = [False] * n

    while not all(swapped):
        i = random.randrange(n)
        j = random.randrange(n)
        deck[i], deck[j] = deck[j], deck[i]
        swapped[i] = True
        swapped[j] = True


def Knuth_shuffle(deck) -> None:
    "Knuth's INPLACE shuffling algorithm."
    for i in range(len(deck) - 1):
        j = random.randrange(i, len(deck))
        deck[i], deck[j] = deck[j], deck[i]


def compare_shuffles(n=100_000, deck_size=4):
    """Compare permutation frequencies for the three shuffle algorithms.
    random.shuffle = knuth, while teacher's clearly biased.
    """
    for shuffle_fn in (random.shuffle, Knuth_shuffle, teacher_shuffle):
        counts = Counter()

        for _ in range(n):
            deck = list(range(deck_size))
            shuffle_fn(deck)
            counts[tuple(deck)] += 1

        print(shuffle_fn.__name__)
        for permutation, count in sorted(counts.items()):
            print(permutation, count)

        # TODO update printout
        # deck size, possible #permutations, probability
        # realized frequencies of the permutations


def print_probability(n=1_000_000):
    """show the probability of each hand category.
    The exact value can be found on Wikipedia.
    TODO low: very slow, consider speedups.
    """
    count = Counter()

    for _ in range(int(n/10)):
        count.update([hand_rank(h)[0] for h in deal(10)])

    print("Probability of different hand categories:")
    for i in range(9):
        print(i, f"{100*count[i]/n}%")


def test_poker():
    """Test all the poker functions.
    Written in the natural progression order, from basic vocab to final target.
    The tests should form a complete usage demonstration.

    TODO (low): more shuffling tests
    """

    # ---------------------------------------------------------------------------
    # Hand examples: one for each category.
    # A single deck, 52 cards; suits are unranked (S, H, C, D), ranks from
    # high to low: A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2.  T stands for 10,
    # so each card is a single alphanumeric object.
    # Each hand is drawn from a separate deck: no duplicate within a hand,
    # but the same card may appear in two different hands.
    # ---------------------------------------------------------------------------

    sf = "6C 7C 8C 9C TC".split()  # straight flush
    fk = "9D 9H 9S 9C 7D".split()  # four of a kind
    fh = "TD TC TH 7C 7D".split()  # full house
    fl = "2S 3S 5S 7S 8S".split()  # flush
    st = "4S 5H 6C 7D 8S".split()  # straight
    tk = "2S 2H 2C 7D 8S".split()  # three of a kind
    tp = "2S 2H 5C 5D 8S".split()  # two pairs
    op = "2S 2H 5C 7D 8S".split()  # one pair
    hc = "2S 3H 5C 7D 8S".split()  # high card

    HANDS = [sf, fk, fh, fl, st, tk, tp, op, hc]


    # --- validate -------------------------------------------------------
    h1 = ['2S', '4S', '5S', '6S', '7S', '8S']  # 6 cards
    h2 = ['4S', '4S', '6S', '7S', '8S']        # duplicate cards
    h3 = ['4M', '4S', '6S', '7S', '8S']        # unrecognized suit
    h4 = ['0S', '5S', '6S', '7S', '8S']        # unrecognized rank
    h5 = ['4', '4S', '6S', '7S', '8S']         # invalid card format

    assert [validate(c) for c in HANDS] == [True] * 9
    assert [validate(c) for c in [h1, h2, h3, h4, h5]] == [False] * 5

    # --- deal -----------------------------------------------------------
    hands = deal(10, shuffle_fn=random.shuffle)
    assert len(hands) == 10
    assert all(len(h)==5 for h in hands)
    assert all(validate(h) for h in hands)

    # --- shuffle functions
    deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
    for shuffle_fn in (Knuth_shuffle, teacher_shuffle):
        shuffled_deck = deck[:]
        assert shuffle_fn(shuffled_deck) is None
        assert len(shuffled_deck) == len(deck)
        assert sorted(shuffled_deck) == sorted(deck)


    # --- card_ranks -----------------------------------------------------
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert card_ranks(fl) == [8, 7, 5, 3, 2]
    assert card_ranks(st) == [8, 7, 6, 5, 4]
    assert card_ranks(tk) == [8, 7, 2, 2, 2]
    assert card_ranks(tp) == [8, 5, 5, 2, 2]
    assert card_ranks(op) == [8, 7, 5, 2, 2]
    assert card_ranks(hc) == [8, 7, 5, 3, 2]
    assert card_ranks(['AC', '3D', '4S', 'KH']) == [14, 13, 4, 3]

    # --- straight -------------------------------------------------------
    assert straight([8, 7, 6, 5, 4]) == True
    assert straight([8, 7, 7, 5, 4]) == False

    # --- flush ----------------------------------------------------------
    assert flush(sf) == True
    assert flush(fh) == False
    assert flush(fl) == True
    assert flush(st) == False

    # --- kind -----------------------------------------------------------
    r1 = [9, 9, 9, 9, 7]  # 4k
    r2 = [9, 9, 9, 7, 7]  # fh
    r3 = [9, 9, 9, 8, 7]  # 3k
    r4 = [8, 7, 5, 2, 2]  # op
    r5 = [8, 7, 5, 3, 2]  # hc
    r6 = [8, 5, 5, 2, 2]  # tp

    fkranks = card_ranks(fk)

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7

    assert kind(4, r1) == 9
    assert kind(4, r2) == None
    assert kind(3, r2) == 9
    assert kind(3, r3) == 9
    assert kind(3, r4) == None
    assert kind(2, r2) == 7
    assert kind(2, r4) == 2
    assert kind(2, r6) == 5
    assert kind(2, r5) == None
    assert kind(1, r1) == 7  # only for single card in 4k

    # --- two_pair -------------------------------------------------------
    p1 = [8, 5, 5, 2, 2]  # two pair
    p2 = [8, 6, 5, 2, 2]  # one pair
    p3 = [8, 6, 5, 3, 2]  # high card

    assert two_pair(p1) == (5, 2)
    assert two_pair(p2) == None
    assert two_pair(p3) == None

    # --- hand_rank ------------------------------------------------------
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    assert hand_rank(fl) == (5, [8, 7, 5, 3, 2])
    assert hand_rank(st) == (4, 8)
    assert hand_rank(tk) == (3, 2, [8, 7, 2, 2, 2])
    assert hand_rank(tp) == (2, (5, 2), [8, 5, 5, 2, 2])
    assert hand_rank(op) == (1, 2, [8, 7, 5, 2, 2])
    assert hand_rank(hc) == (0, [8, 7, 5, 3, 2])

    # --- allmax ---------------------------------------------------------
    assert allmax([1, 2, 3, 4, 5]) == [5]
    assert allmax([1, 2, 3, 4, 5], key=lambda x: x % 3) == [2, 5]
    assert allmax([1, 2, 3, 4, 5], key=lambda x: x % 2) == [1, 3, 5]


    # --- poker ----------------------------------------------------------
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]

    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([fh]) == [fh]

    print("All poker tests passed.")


if __name__ == "__main__":

    test_poker()
    print_probability()
    compare_shuffles()
