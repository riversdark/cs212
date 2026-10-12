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


from math import factorial
from itertools import permutations

PETS = ['dog', 'snail', 'zebra', 'fox', 'horse']
NATIONALITIES = ['English', 'Spanish', 'Norwegian', 'Japanes', 'Ukrainian']
SMOKES = ['Parliament', 'Old Gold', 'Lucky Strike', 'Kools', 'Chesterfields']
COLORS = ['red', 'green', 'blue', 'yellow', 'ivory']
BEVERAGES = ['tea', 'milk', 'water', 'orange juice', 'coffee']

PROPERTIES = [PETS, NATIONALITIES, SMOKES, COLORS, BEVERAGES]
HOUSES = [1, 2, 3, 4, 5]

def F(choices) -> list[tuple[int, ...]]:
    "All possible house orderings."
    return list(permutations(choices))

def test_zebra():

    # properties
    assert len(PETS) == 5
    assert len(NATIONALITIES) == 5
    assert len(SMOKES) == 5
    assert len(COLORS) == 5
    assert len(BEVERAGES) == 5

    assert len(PROPERTIES) == 5
    assert len(HOUSES) == 5

    # F ordering
    assert all(len(ord) == 5 for ord in F(HOUSES))
    assert len(F(PETS)) == 120
    assert len(F(NATIONALITIES)) == 120
    assert len(F(SMOKES)) == 120
    assert len(F(COLORS)) == 120
    assert len(F(HOUSES)) == 120

    print("zebra tests passed.")

if __name__ == "__main__":

    print(f"total possible orderings, factorial(5)^5 = {factorial(5)**5}.")
    test_zebra()

    orderings_color = F(COLORS)
    for (red, green, blue, yellow, ivory) in orderings_color:
        ...
