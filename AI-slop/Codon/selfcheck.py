"""Run with Codon 0.19.3: codon run selfcheck.py."""

from convolution import convolution
from cpp.LazySegmentTree import LazySegmentTree
from cpp.WaveletMatrix import WaveletMatrix
from cpp.WaveletMatrixSegmentTree import WaveletMatrixSegmentTree
from cpp.Range_Parallel_UnionFind import RangeParallelUnionFind
from cpp.OnlineTwoEdgeConnectivity import OnlineTwoEdgeConnectivity
from cpp.PSL import Prod_of_Sum_of_Log, Prod_of_Sum_of_Log_test
from cpp.Sum_of_Prod_of_Root import Sum_of_Prod_of_Root, Sum_of_Prod_of_Root_test
from Python.PriorityQue import PriorityQue
from Python.convex import convex
from Python.isprime import is_prime


def pair_op(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def pair_e() -> tuple[int, int]:
    return (0, 0)


def add_comp(a: int, b: int) -> int:
    return a + b


def pair_add(f: int, x: tuple[int, int]) -> tuple[int, int]:
    return (x[0] + f * x[1], x[1])


def zero() -> int:
    return 0


def add(a: int, b: int) -> int:
    return a + b


assert convolution([1, 2, 3], [4, 5]) == [4, 13, 22, 15]

seg = LazySegmentTree([(1, 1), (2, 1), (3, 1)], pair_op, pair_e, add_comp, pair_add, zero)
seg.apply(1, 3, 5)
assert seg.prod(0, 3) == (16, 3)

wm = WaveletMatrix([2, 0, 3, 1])
assert wm.mex0(0, 4) == 4
assert wm.range_kth_min(0, 4, 2) == 2
assert wm.select(0, 3) == 2

wmst = WaveletMatrixSegmentTree([(2, 5), (0, 7), (2, 11)], add, zero)
assert wmst.range_prod(0, 3, 2, 3) == 16
wmst.updata(2, 13)
assert wmst.range_prod(0, 3, 2, 3) == 18

ruf = RangeParallelUnionFind(4, [1, 2, 3, 4])
ruf.query(2, 0, 2)
assert ruf.get_global_value() == 11

tec = OnlineTwoEdgeConnectivity(3)
tec.add_edge(0, 1)
tec.add_edge(1, 2)
tec.add_edge(2, 0)
assert tec.query(0, 2, 2) == 1
assert tec.query(0, 2) == 2
assert tec.first_two_edge_connected_time(0, 2) == 3

for n in range(2, 50):
    assert Prod_of_Sum_of_Log(n, 3) == Prod_of_Sum_of_Log_test(n, 3)
    assert Sum_of_Prod_of_Root(n, 998244353) == Sum_of_Prod_of_Root_test(n, 998244353)

heap = PriorityQue([])
heap.append(3)
heap.append(1)
assert heap.pop() == 1
assert len(convex([(0, 0), (2, 0), (1, 1), (1, 0)])) == 3
assert is_prime(2305843009213693951)
