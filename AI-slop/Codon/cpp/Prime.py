"""Codon entry point for the classes collected in cpp/Prime.cpp.

Each implementation lives in the matching small module in this directory.
Codon exposes the collected classes as direct imports from this module.
"""

from CumTable import CumulativeTable
from FenwickTree import BIT
from TernaryIndexedTree import TIT
from PartialPersistentArray import PartiallyPersistentArray
from PersistentStack import PersistentStack
from SegmentTree import SegmentTree
from LazySegmentTree import LazySegmentTree
from FullyIndexableDictionary import FullyIndexableDictionary
from WaveletMatrix import WaveletMatrix
from WaveletMatrixSegmentTree import WaveletMatrixSegmentTree
from BinaryTreeSet import BinaryTreeSet
from BinaryTrie import BinaryTrie
from UnionFind import UnionFind
from DynamicUnionFind import DynamicUnionFind
from PartiallyPersistentUnionFind import PartiallyPersistentUnionFind
from PartiallyPersistentUnionFind2 import PartiallyPersistentUnionFind as PartiallyPersistentUnionFind_PartiallyPersistentArray
from Permutation import Permutation, pow as permutation_pow, powpow as permutation_powpow, product as permutation_product
from isqrt import isqrt
from next_partation import next_partation
from Area_of_Union_of_Rectangles import AreaOfUnionOfRectangles
from PrimePresets import RSQ_RUQ, RSQ_RUQ_S, RSQ_RUQ_F, Affinell, Affinell_S, Affinell_F, Affinemint, Affinemint_S, Affinemint_F, ADD_DIV_MAX_RESTORE, ADD_DIV_MAX_RESTORE_S, ADD_DIV_MAX_RESTORE_F


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def exgcd(a: int, b: int) -> tuple[int, int]:
    x0, x1 = 1, 0
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
    return x0, a


def _mulmod(a: int, b: int, n: int) -> int:
    return int(u128(a) * u128(b) % u128(n))


def powll(a: int, d: int, n: int) -> int:
    ans = 1
    a %= n
    while d:
        if d & 1:
            ans = _mulmod(ans, a, n)
        a = _mulmod(a, a, n)
        d >>= 1
    return ans


def MillerRabin(N: int, arr: list[int]) -> bool:
    if N < 2:
        return False
    s = (N - 1).__cttz__()
    d = (N - 1) >> s
    for a in arr:
        if a % N == 0:
            continue
        x = powll(a % N, d, N)
        if x == 1 or x == N - 1:
            continue
        for _ in range(s - 1):
            x = _mulmod(x, x, N)
            if x == N - 1:
                break
        else:
            return False
    return True


def isprime(N: int) -> bool:
    if N <= 1:
        return False
    if N == 2:
        return True
    if N & 1 == 0:
        return False
    if N < 4759123141:
        return MillerRabin(N, [2, 7, 61])
    return MillerRabin(N, [2, 325, 9375, 28178, 450775, 9780504, 1795265022])


# The C++ n3 namespace is represented by this Codon module. Import the
# desired class or function directly from Prime.
