"""CS212 - Zebra Puzzle.

1 There are five houses.
2 The Englishman lives in the red house.
3 The Spaniard owns the dog.
4 Coffee is drunk in the green house.
5 The Ukrainian drinks tea.
6 The green house is immediately to the right of the ivory house.
7 The Old Gold smoker owns snails.
8 Kools are smoked in the yellow house.
9 Milk is drunk in the middle house.
10 The Norwegian lives in the first house.
11 The man who smokes Chesterfields lives in the house next to the man with the fox.
12 Kools are smoked in a house next to the house where the horse is kept.
13 The Lucky Strike smoker drinks orange juice.
14 The Japanese smokes Parliaments.
15 The Norwegian lives next to the blue house.

Q: Who drinks water? Who owns the zebra?

Each house is painted a different color, and their inhabitants are of different
nationalities, own different pets, drink different beverages and smoke different
brands of American cigarettes.
"""
from statistics import mean
import time

import itertools
from math import factorial

HOUSES = [1, 2, 3, 4, 5]
orderings = list(itertools.permutations(HOUSES))

def estimate_runtime():
    "estimate total iterations, expected runtime, etc."
    txt = f"""\nEstimating runtime:
    Each property has {factorial(5)} different arrangements.
    Back of envolope iteration estimation...
    fac(5)**5 -> 120**5 -> 100**5 -> 10**10 -> 10 billion
    Actual number: factorial(5)^5 = {factorial(5)**5}, about 24 billion.
    compelexity analysis for modern PCs...
    happy millions, sad trillions, and uncertain billions
    On a 2.4G Hz computer, assuming each iteration takes 1000 computer instructions...
    total runtime 1000 * (24/2.4) = 10K seconds, about 3 hours.
    \n"""
    print(txt)

def imright(h1, h2):
    "House 1 is immediate right to house 2."
    return h1-h2 == 1

def nextto(h1, h2):
    "House 1 is next to house 2."
    return abs(h1-h2) == 1

def c(seq):
    """Turn seq into generator, remember how many times it's called.
    """
    c.starts += 1
    for item in seq:
        c.items += 1
        yield item

c.starts, c.items = 0, 0

def zebra_puzzle():
    """get house number for water and zebra.
    1. approaches to assign properties to houses: sets, classes, assignments.
        assigning house numbers directly to properties.
    2. using generator expression: stop early, less indentation, easier edit.
    3. ordering for/if statements to eliminate impossible combos as early as possible.
    """
    return next(
        (WATER, ZEBRA)
        for (red, green, ivory, blue, yellow) in c(orderings)
        if imright(green, ivory)
        for (en, es, ukr, jap, nor) in c(orderings)
        if nor == 1
        if en is red
        if nextto(nor, blue)
        for (coffee, tea, milk, WATER, ojuice) in c(orderings)
        if milk == 3
        if coffee is green
        if ukr is tea
        for (Kools, LuckyStrike, Chesterfields, OldGold, Parliaments) in c(orderings)
        if Kools is yellow
        if LuckyStrike is ojuice
        if jap is Parliaments
        for (dog, fox, snails, horse, ZEBRA) in c(orderings)
        if es is dog
        if OldGold is snails
        if nextto(Chesterfields, fox)
        if nextto(Kools, horse)
    )

def timeit(fn, *args):
    """Timing the function execution.
    using higher order functions for functions with side effects.
    using star arguments for easy packing & unpacking.
    making repeated measurements moves CS from math to be more like science..
    this helps to reduce errors, randomness, and external effects
    """

    t0 = time.time()
    res = fn(*args)
    t1 = time.time()

    return t1-t0, res

def timethem(n, fn, *args):
    """Time function for n times, return (min, mean, max) time.
    3 order function, fn -> timeit -> timethem
    """
    res = [timeit(fn, *args)[0] for _ in range(n)]
    return min(res), mean(res), max(res)

def instrument_fn(fn, *args):
    c.starts, c.items = 0, 0
    res = fn(*args)
    print(f"Function {fn.__name__} got {res} with {c.starts} iters over {c.items} items.")

def test_zebra():

    assert len(HOUSES) == 5
    assert len(orderings) == 120

    h1, h2 = 1, 2
    assert h1 is not h2
    assert h1 != h2

    assert imright(h1, h2) is False
    assert imright(h2, h1) is True
    assert nextto(h1, h2) is True
    assert nextto(h2, h1) is True

    assert zebra_puzzle() == (1, 5)

    print("zebra tests passed.")

if __name__ == "__main__":

    estimate_runtime()
    test_zebra()
    print(zebra_puzzle())
    print(timeit(zebra_puzzle))
    print(timethem(10, zebra_puzzle))
    instrument_fn(zebra_puzzle)
