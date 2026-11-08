"""CS212 cryptarithmetics.
Find ALL numeral combinations (0-9) that satisfy the equation ODD+ODD=EVEN

O cannot be 0.
E can only be 1 for any valid solution.
Each repeated letter (ODE) corresponds to the same numeral value.
Repetitions among ODEVN are allowed.
"""
from itertools import product
from zebra import timeit, timethem

def candidates():
    """A generator for 10-digit numerals encoding, e.g. '3232232234'.
    No pre-applied requirements checking, each digit can be any of [0-9].
    Total iterations = 10^10 = 10 Billion.
    """
    for digits in product('0123456789', repeat=10):
        yield "".join(digits)

def candidates2():
    """A generator for 5-letter numerals encoding, e.g. ODEVN=12345.
    Then expand the 5 letters to 10 digits.
    Total iterations = 10^5 = 100K, 100K times speedup.
    """
    for (O, D, E, V, N) in product('0123456789', repeat=5):
        yield f"{O}{D}{D}{O}{D}{D}{E}{V}{E}{N}"

def candidates3():
    """A generator for 4-letter numerals encoding, e.g. ODVN=1234.
    Combined with E=1, then expand the 5 letters to 10 digits.
    Total iterations = 10^4 = 10K, 1M times speedup.
    """
    E = '1'
    for (O, D, V, N) in product('0123456789', repeat=4):
        yield f"{O}{D}{D}{O}{D}{D}{E}{V}{E}{N}"

def insert_ops(nums:str) -> str:
    """Insert operators so ODDODDEVEN -> ODD+ODD==EVEN"""
    return f"{nums[:3]}+{nums[3:6]}=={nums[6:]}"

def crypta_puzzle():
    """Solving the puzzle by brute-force enumeration."""
    return [insert_ops(nums)
            for nums in candidates3()
            if nums[0] == nums[3] != '0' # O not 0
            if nums[1] == nums[2] == nums[4] == nums[5] # D
            if nums[6] == nums[8] == '1' # E is 1
            if eval(insert_ops(nums))    # fragile and inefficient, but works
            ]

def test():

    cand = candidates()
    assert len(next(cand)) == 10
    assert insert_ops('3232232234') == '323+223==2234'
    print("Crypta tests passed!")

if __name__ == "__main__":

    test()
    print(crypta_puzzle())
    print(timeit(crypta_puzzle))
    print(timethem(10, crypta_puzzle))
