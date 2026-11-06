def _popcount64(x: int) -> int:
    x -= (x >> 1) & 0x5555555555555555
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    return (x * 0x0101010101010101 >> 56) & 255


class FullyIndexableDictionary:
    sz: int
    data: list[int]
    BT: list[int]
    popcount: int
    is_builded: bool

    def __init__(self, sz: int):
        self.sz = sz
        self.data = [0] * ((sz + 63) >> 6)
        self.BT = [0] * (len(self.data) + 1)
        self.popcount = 0
        self.is_builded = False

    def set(self, i: int, b: int):
        assert not self.is_builded and 0 <= i < self.sz
        if b == 1:
            self.data[i >> 6] |= 1 << (i & 63)
        else:
            self.data[i >> 6] &= ~(1 << (i & 63))

    def test(self, i: int) -> bool:
        assert 0 <= i < self.sz
        return ((self.data[i >> 6] >> (i & 63)) & 1) != 0

    def __getitem__(self, i: int) -> int:
        return int(self.test(i))

    def build(self):
        assert not self.is_builded
        self.is_builded = True
        s = 0
        for i in range(len(self.data)):
            self.BT[i] = s
            s += _popcount64(self.data[i])
        self.BT[len(self.data)] = s
        self.popcount = s

    def rank(self, n: int, b: int) -> int:
        assert self.is_builded and 0 <= n <= self.sz
        i = n >> 6
        ones = self.BT[i]
        if i < len(self.data):
            ones += _popcount64(self.data[i] & ((1 << (n & 63)) - 1))
        return ones if b else n - ones

    def rank_all(self, b: int) -> int:
        return self.popcount if b else self.sz - self.popcount

    def select(self, n: int, b: int) -> int:
        if n < 0 or n >= self.rank_all(b):
            return -1
        lo, hi = 0, self.sz
        while lo < hi:
            mid = (lo + hi) >> 1
            if self.rank(mid + 1, b) > n:
                hi = mid
            else:
                lo = mid + 1
        return lo

class SegmentTree[T]:
    array: list[T]
    op: Callable[[T, T], T]
    e: Callable[[], T]
    n: int
    cap: int

    def __init__(self, array: list[T], op: Callable[[T, T], T], e: Callable[[], T]):
        self.n = len(array)
        self.cap = 1
        while self.cap < self.n:
            self.cap <<= 1
        self.op = op
        self.e = e
        self.array = [e() for _ in range(2 * self.cap)]
        for i in range(self.n):
            self.array[self.cap + i] = array[i]
        for i in range(self.cap - 1, 0, -1):
            self.array[i] = op(self.array[i << 1], self.array[i << 1 | 1])

    def get(self, i: int) -> T:
        return self.array[self.cap + i]

    def write(self, i: int, value: T):
        i += self.cap
        self.array[i] = value
        while i > 1:
            i >>= 1
            self.array[i] = self.op(self.array[i << 1], self.array[i << 1 | 1])

    def inplace_op(self, i: int, value: T):
        self.write(i, self.op(self.get(i), value))

    def prod(self, l: int, r: int) -> T:
        a = self.e()
        b = self.e()
        l += self.cap
        r += self.cap
        while l < r:
            if l & 1:
                a = self.op(a, self.array[l])
                l += 1
            if r & 1:
                r -= 1
                b = self.op(self.array[r], b)
            l >>= 1
            r >>= 1
        return self.op(a, b)

    def size(self) -> int:
        return self.n


class WaveletMatrixSegmentTree[V]:
    sz: int
    degits: int
    data: list[FullyIndexableDictionary]
    segs: list[SegmentTree[V]]
    keys_array: list[int]
    values_array: list[V]
    op: Callable[[V, V], V]
    e: Callable[[], V]

    def __init__(self, array: list[tuple[int, V]], op: Callable[[V, V], V], e: Callable[[], V]):
        self.sz = len(array)
        self.op = op
        self.e = e
        self.keys_array = [p[0] for p in array]
        self.values_array = [p[1] for p in array]
        maximum = max(self.keys_array) if self.keys_array else 0
        assert all(x >= 0 for x in self.keys_array)
        self.degits = 0
        while maximum:
            self.degits += 1
            maximum >>= 1
        if self.degits == 0:
            self.degits = 1
        self.data = [FullyIndexableDictionary(self.sz) for _ in range(self.degits)]
        self.segs = [SegmentTree(self.values_array, op, e) for _ in range(self.degits)]
        a = array[:]
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            zero = []
            one = []
            for i, pair in enumerate(a):
                bit = (pair[0] >> d) & 1
                bv.set(i, bit)
                if bit:
                    one.append(pair)
                else:
                    zero.append(pair)
            bv.build()
            a = zero + one
            self.segs[d] = SegmentTree([pair[1] for pair in a], op, e)

    def keys(self, i: int) -> int:
        return self.keys_array[i]

    def values(self, i: int) -> V:
        return self.values_array[i]

    def count_key(self, l: int, r: int, x: int) -> int:
        assert 0 <= l <= r <= self.sz
        if x < 0 or x >= 1 << self.degits:
            return 0
        for d in range(self.degits - 1, -1, -1):
            bit = (x >> d) & 1
            bv = self.data[d]
            off = bv.rank_all(0) if bit else 0
            l = off + bv.rank(l, bit)
            r = off + bv.rank(r, bit)
        return r - l

    def rank_key(self, i: int, c: int) -> int:
        return self.count_key(0, i, c)

    def select(self, i: int, x: int) -> int:
        if i < 0 or x < 0 or x >= 1 << self.degits:
            return -1
        l, r = 0, self.sz
        for d in range(self.degits - 1, -1, -1):
            bit = (x >> d) & 1
            bv = self.data[d]
            off = bv.rank_all(0) if bit else 0
            l = off + bv.rank(l, bit)
            r = off + bv.rank(r, bit)
        if i >= r - l:
            return -1
        i += l
        for d in range(self.degits):
            bit = (x >> d) & 1
            bv = self.data[d]
            i = bv.select(i - (bv.rank_all(0) if bit else 0), bit)
        return i

    def range_kth_min(self, l: int, r: int, i: int) -> int:
        if i < 0 or i >= r - l:
            return -1
        ans = 0
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            zeros = bv.rank(r, 0) - bv.rank(l, 0)
            if i < zeros:
                l = bv.rank(l, 0)
                r = bv.rank(r, 0)
            else:
                i -= zeros
                ans |= 1 << d
                off = bv.rank_all(0)
                l = off + bv.rank(l, 1)
                r = off + bv.rank(r, 1)
        return ans

    def range_kth_max(self, l: int, r: int, i: int) -> int:
        return self.range_kth_min(l, r, r - l - 1 - i)

    def _less(self, l: int, r: int, x: int) -> int:
        if x <= 0:
            return 0
        if x >= 1 << self.degits:
            return r - l
        ans = 0
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            bit = (x >> d) & 1
            if bit:
                ans += bv.rank(r, 0) - bv.rank(l, 0)
            off = bv.rank_all(0) if bit else 0
            l = off + bv.rank(l, bit)
            r = off + bv.rank(r, bit)
        return ans

    def range_freq(self, l: int, r: int, x: int, y: int) -> int:
        return 0 if y <= x else self._less(l, r, y) - self._less(l, r, x)

    def _range_prod(self, l: int, r: int, d: int, base: int, x: int, y: int) -> V:
        if l == r or d < 0:
            return self.e()
        bv = self.data[d]
        off = bv.rank_all(0)
        l0, r0 = bv.rank(l, 0), bv.rank(r, 0)
        l1, r1 = off + bv.rank(l, 1), off + bv.rank(r, 1)
        half = 1 << d
        if x <= base and base + half <= y:
            a = self.segs[d].prod(l0, r0)
        elif x < base + half and y > base:
            a = self._range_prod(l0, r0, d - 1, base, x, y) if d > 0 else self.e()
        else:
            a = self.e()
        if x <= base + half and base + (half << 1) <= y:
            b = self.segs[d].prod(l1, r1)
        elif x < base + (half << 1) and y > base + half:
            b = self._range_prod(l1, r1, d - 1, base + half, x, y) if d > 0 else self.e()
        else:
            b = self.e()
        return self.op(a, b)

    def range_prod(self, l: int, r: int, x: int, y: int) -> V:
        assert 0 <= l <= r <= self.sz
        if y <= x:
            return self.e()
        return self._range_prod(l, r, self.degits - 1, 0, x, y)

    def updata(self, ind: int, x: V):
        assert 0 <= ind < self.sz
        self.values_array[ind] = x
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            bit = bv[ind]
            ind = (bv.rank_all(0) if bit else 0) + bv.rank(ind, bit)
            self.segs[d].write(ind, x)

    def successor(self, l: int, r: int, v: int) -> int:
        return self.range_kth_min(l, r, self._less(l, r, v))

    def predecessor(self, l: int, r: int, v: int) -> int:
        return self.range_kth_min(l, r, self._less(l, r, v) - 1)

    def size(self) -> int:
        return self.sz
