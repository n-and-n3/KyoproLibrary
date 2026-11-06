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


class WaveletMatrix:
    sz: int
    degits: int
    data: list[FullyIndexableDictionary]

    def __init__(self, array: list[int]):
        self.sz = len(array)
        maximum = max(max(array), len(array)) if array else 0
        assert minimum_nonnegative(array)
        self.degits = 0
        while maximum:
            self.degits += 1
            maximum >>= 1
        if self.degits == 0:
            self.degits = 1
        self.data = [FullyIndexableDictionary(self.sz) for _ in range(self.degits)]
        a = array[:]
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            zero = []
            one = []
            for i, x in enumerate(a):
                bit = (x >> d) & 1
                bv.set(i, bit)
                if bit:
                    one.append(x)
                else:
                    zero.append(x)
            bv.build()
            a = zero + one

    def access(self, i: int) -> int:
        assert 0 <= i < self.sz
        ans = 0
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            bit = bv[i]
            ans = ans << 1 | bit
            i = (bv.rank_all(0) if bit else 0) + bv.rank(i, bit)
        return ans

    def __getitem__(self, i: int) -> int:
        return self.access(i)

    def count(self, l: int, r: int, x: int) -> int:
        assert 0 <= l <= r <= self.sz
        if x < 0 or x >= 1 << self.degits:
            return 0
        for d in range(self.degits - 1, -1, -1):
            bit = (x >> d) & 1
            bv = self.data[d]
            offset = bv.rank_all(0) if bit else 0
            l = offset + bv.rank(l, bit)
            r = offset + bv.rank(r, bit)
        return r - l

    def rank(self, i: int, c: int) -> int:
        return self.count(0, i, c)

    def select(self, i: int, x: int) -> int:
        if i < 0 or x < 0 or x >= 1 << self.degits:
            return -1
        l, r = 0, self.sz
        for d in range(self.degits - 1, -1, -1):
            bit = (x >> d) & 1
            bv = self.data[d]
            offset = bv.rank_all(0) if bit else 0
            l = offset + bv.rank(l, bit)
            r = offset + bv.rank(r, bit)
        if i >= r - l:
            return -1
        i += l
        for d in range(self.degits):
            bit = (x >> d) & 1
            bv = self.data[d]
            i = bv.select(i - (bv.rank_all(0) if bit else 0), bit)
        return i

    def range_kth_min(self, l: int, r: int, i: int) -> int:
        assert 0 <= l <= r <= self.sz
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
        assert 0 <= l <= r <= self.sz
        return 0 if y <= x else self._less(l, r, y) - self._less(l, r, x)

    def successor(self, l: int, r: int, v: int) -> int:
        return self.range_kth_min(l, r, self._less(l, r, v))

    def predecessor(self, l: int, r: int, v: int) -> int:
        return self.range_kth_min(l, r, self._less(l, r, v) - 1)

    def mex0(self, l: int, r: int) -> int:
        assert 0 <= l <= r <= self.sz
        left, right = l, r
        ans = 0
        for d in range(self.degits - 1, -1, -1):
            bv = self.data[d]
            zeros = bv.rank(right, 0) - bv.rank(left, 0)
            if zeros < 1 << d:
                left = bv.rank(left, 0)
                right = bv.rank(right, 0)
            else:
                ans |= 1 << d
                off = bv.rank_all(0)
                left = off + bv.rank(left, 1)
                right = off + bv.rank(right, 1)
        return ans

    def mex1(self, l: int, r: int) -> int:
        return min(self.range_kth_min(0, l, 0) if l else self.sz, self.range_kth_min(r, self.sz, 0) if r < self.sz else self.sz)

    def size(self) -> int:
        return self.sz


def minimum_nonnegative(array: list[int]) -> bool:
    for x in array:
        if x < 0:
            return False
    return True
