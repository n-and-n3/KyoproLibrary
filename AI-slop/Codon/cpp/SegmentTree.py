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
