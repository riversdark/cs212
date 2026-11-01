"""CS212 cryptarithmetics.
Find ALL numeral combinations (0-9) that satisfy the equation ODD+ODD=EVEN

O cannot be 0.
E can only be 1.
repeated letters correspond to the same numeral value, O, D, E.
"""
from zebra import timeit, timethem

def random_outcome() -> str:
    """A generator for 10-digit numerals generation. e.g. '3232232234'.
    No pre-applied requirements checking, each digit can be any of [0-9].
    """
    yield ...

def insert_ops(nums:str) -> str:
    """Insert math operators to form proper math expressions.
    e.g. '3232232234' -> '323+223==2234'
    """
    return ...


def crypta_puzzle():
    """Solving the puzzle by brute-force enumeration.
    Q:  how to loop with generator?
    """
    rog = random_outcome()

    return [nums
            for nums in rog
            if nums[0] == nums[3] != 0 # O not 0
            if nums[1] == nums[2] == nums[4] == nums[5] # D
            if nums[6] == nums[8] == 1 # E is 1
            if eval(insert_ops(nums)) is True
            ]

def test_crypta():

    print("Crypta tests passed!")

if __name__ == "__main__":

    test_crypta()
    print(crypta_puzzle)
    print(timeit(crypta_puzzle))
    print(timethem(10, crypta_puzzle))
