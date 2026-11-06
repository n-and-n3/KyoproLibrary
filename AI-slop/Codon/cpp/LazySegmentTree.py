class LazySegmentTree[S, F]:
    data: list[S]
    lazy: list[F]
    op: Callable[[S, S], S]
    e: Callable[[], S]
    composition: Callable[[F, F], F]
    mapping: Callable[[F, S], S]
    id: Callable[[], F]
    sz: int
    N: int
    logN: int

    def __init__(self, array: list[S], op: Callable[[S, S], S], e: Callable[[], S], composition: Callable[[F, F], F], mapping: Callable[[F, S], S], id: Callable[[], F]):
        self.sz = len(array)
        self.N = 1
        self.logN = 0
        while self.N < self.sz:
            self.N <<= 1
            self.logN += 1
        self.op = op
        self.e = e
        self.composition = composition
        self.mapping = mapping
        self.id = id
        self.data = [e() for _ in range(2 * self.N)]
        self.lazy = [id() for _ in range(self.N)]
        for i in range(self.sz):
            self.data[self.N + i] = array[i]
        for i in range(self.N - 1, 0, -1):
            self._update(i)

    def _update(self, i: int):
        self.data[i] = self.op(self.data[i << 1], self.data[i << 1 | 1])

    def _all_apply(self, i: int, f: F):
        self.data[i] = self.mapping(f, self.data[i])
        if i < self.N:
            self.lazy[i] = self.composition(f, self.lazy[i])

    def point_propagate(self, i: int):
        f = self.lazy[i]
        self._all_apply(i << 1, f)
        self._all_apply(i << 1 | 1, f)
        self.lazy[i] = self.id()

    def line_propagate(self, ind: int):
        assert 0 <= ind <= self.sz
        if ind == self.sz:
            return
        ind += self.N
        for k in range(self.logN, 0, -1):
            self.point_propagate(ind >> k)

    def all_propagate(self):
        for i in range(1, self.N):
            self.point_propagate(i)

    def get(self, i: int) -> S:
        assert 0 <= i < self.sz
        i += self.N
        for k in range(self.logN, 0, -1):
            self.point_propagate(i >> k)
        return self.data[i]

    def write(self, i: int, x: S):
        assert 0 <= i < self.sz
        i += self.N
        for k in range(self.logN, 0, -1):
            self.point_propagate(i >> k)
        self.data[i] = x
        for k in range(1, self.logN + 1):
            self._update(i >> k)

    def prod(self, l: int, r: int) -> S:
        assert 0 <= l <= r <= self.sz
        if l == r:
            return self.e()
        l += self.N
        r += self.N
        for k in range(self.logN, 0, -1):
            if ((l >> k) << k) != l:
                self.point_propagate(l >> k)
            if ((r >> k) << k) != r:
                self.point_propagate((r - 1) >> k)
        a = self.e()
        b = self.e()
        while l < r:
            if l & 1:
                a = self.op(a, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                b = self.op(self.data[r], b)
            l >>= 1
            r >>= 1
        return self.op(a, b)

    def prod_all(self) -> S:
        return self.data[1]

    def apply(self, l: int, r: int, f: F):
        assert 0 <= l <= r <= self.sz
        if l == r:
            return
        l += self.N
        r += self.N
        for k in range(self.logN, 0, -1):
            if ((l >> k) << k) != l:
                self.point_propagate(l >> k)
            if ((r >> k) << k) != r:
                self.point_propagate((r - 1) >> k)
        l0, r0 = l, r
        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1
        for k in range(1, self.logN + 1):
            if ((l0 >> k) << k) != l0:
                self._update(l0 >> k)
            if ((r0 >> k) << k) != r0:
                self._update((r0 - 1) >> k)
