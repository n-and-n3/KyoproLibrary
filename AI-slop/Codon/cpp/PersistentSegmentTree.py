class _PSTStore[T]:
    left: list[int]
    right: list[int]
    value: list[T]

    def __init__(self, example: T):
        self.left = []
        self.right = []
        self.value = []

    def node(self, l: int, r: int, x: T) -> int:
        i = len(self.value)
        self.left.append(l)
        self.right.append(r)
        self.value.append(x)
        return i


class PersistentSegmentTree[T]:
    store: _PSTStore[T]
    root: int
    n: int
    cap: int
    op: Callable[[T, T], T]
    e: Callable[[], T]

    def __init__(self, array: list[T], op: Callable[[T, T], T], e: Callable[[], T]):
        self.n = len(array)
        self.cap = 1
        while self.cap < self.n:
            self.cap <<= 1
        self.op = op
        self.e = e
        self.store = _PSTStore(e())
        self.root = self._build(0, self.cap, array)

    def __init__(self, store: _PSTStore[T], root: int, n: int, cap: int, op: Callable[[T, T], T], e: Callable[[], T]):
        self.store = store
        self.root = root
        self.n = n
        self.cap = cap
        self.op = op
        self.e = e

    def _build(self, l: int, r: int, array: list[T]) -> int:
        if r - l == 1:
            return self.store.node(-1, -1, array[l] if l < self.n else self.e())
        m = (l + r) >> 1
        a = self._build(l, m, array)
        b = self._build(m, r, array)
        return self.store.node(a, b, self.op(self.store.value[a], self.store.value[b]))

    def clone(self) -> PersistentSegmentTree[T]:
        return PersistentSegmentTree(self.store, self.root, self.n, self.cap, self.op, self.e)

    def copy(self) -> PersistentSegmentTree[T]:
        return self.clone()

    def get(self, i: int) -> T:
        assert 0 <= i < self.n
        p, l, r = self.root, 0, self.cap
        while r - l > 1:
            m = (l + r) >> 1
            if i < m:
                p = self.store.left[p]
                r = m
            else:
                p = self.store.right[p]
                l = m
        return self.store.value[p]

    def _write(self, p: int, l: int, r: int, i: int, x: T) -> int:
        if r - l == 1:
            return self.store.node(-1, -1, x)
        m = (l + r) >> 1
        a = self.store.left[p]
        b = self.store.right[p]
        if i < m:
            a = self._write(a, l, m, i, x)
        else:
            b = self._write(b, m, r, i, x)
        return self.store.node(a, b, self.op(self.store.value[a], self.store.value[b]))

    def write(self, i: int, value: T):
        assert 0 <= i < self.n
        self.root = self._write(self.root, 0, self.cap, i, value)

    def inplace_op(self, i: int, value: T):
        self.write(i, self.op(self.get(i), value))

    def _prod(self, p: int, l: int, r: int, ql: int, qr: int) -> T:
        if qr <= l or r <= ql:
            return self.e()
        if ql <= l and r <= qr:
            return self.store.value[p]
        m = (l + r) >> 1
        a = self._prod(self.store.left[p], l, m, ql, qr)
        b = self._prod(self.store.right[p], m, r, ql, qr)
        return self.op(a, b)

    def prod(self, l: int, r: int) -> T:
        assert 0 <= l <= r <= self.n
        return self._prod(self.root, 0, self.cap, l, r)

    def size(self) -> int:
        return self.n
