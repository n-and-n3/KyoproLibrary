MOD = 998244353


class RangeParallelUnionFind:
    parent: list[int]
    next_v: list[int]
    data: list[int]
    global_value: int
    layers: list[list[int]]
    n: int

    def __init__(self, n: int, v: list[int]):
        assert n == len(v)
        self.n = n
        self.parent = [-1] * n
        self.next_v = list(range(n))
        self.data = [x % MOD for x in v]
        self.global_value = 0
        self.layers = []
        p = 1
        while p <= n:
            self.layers.append([-1] * n)
            p <<= 1

    def root(self, x: int) -> int:
        p = self.parent
        r = x
        while p[r] >= 0:
            r = p[r]
        while p[x] >= 0:
            y = p[x]
            p[x] = r
            x = y
        return r

    def merge(self, x: int, y: int) -> bool:
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.global_value = (self.global_value + self.data[x] * self.data[y]) % MOD
        self.data[x] = (self.data[x] + self.data[y]) % MOD
        self.data[y] = 0
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        self.next_v[x], self.next_v[y] = self.next_v[y], self.next_v[x]
        return True

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def size(self, x: int) -> int:
        return -self.parent[self.root(x)]

    def component(self, v: int) -> list[int]:
        ans = [v]
        x = self.next_v[v]
        while x != v:
            ans.append(x)
            x = self.next_v[x]
        return ans

    def get_global_value(self) -> int:
        return self.global_value

    def _layer_root(self, h: int, x: int) -> int:
        p = self.layers[h]
        r = x
        while p[r] >= 0:
            r = p[r]
        while p[x] >= 0:
            y = p[x]
            p[x] = r
            x = y
        return r

    def _join(self, h: int, a: int, b: int):
        x = self._layer_root(h, a)
        y = self._layer_root(h, b)
        if x == y:
            return
        p = self.layers[h]
        if p[x] > p[y]:
            x, y = y, x
        p[x] += p[y]
        p[y] = x
        if h == 0:
            self.merge(a, b)
        else:
            half = 1 << (h - 1)
            self._join(h - 1, a, b)
            self._join(h - 1, a + half, b + half)

    def query(self, k: int, l: int, r: int):
        assert 0 <= k and 0 <= l <= self.n - k and 0 <= r <= self.n - k
        if k == 0:
            return
        h = 0
        while (1 << (h + 1)) <= k:
            h += 1
        width = 1 << h
        self._join(h, l, r)
        if width < k:
            self._join(h, l + k - width, r + k - width)
