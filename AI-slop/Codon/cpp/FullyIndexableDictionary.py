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
