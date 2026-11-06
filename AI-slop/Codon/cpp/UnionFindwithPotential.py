# cpp/UnionFindwithPotential.cpp only declared an empty struct. This supplies
# the standard weighted Union-Find interface for additive potentials.
class UnionFindwithPotential:
    parent: list[int]
    weight: list[int]
    c: int

    def __init__(self, n: int):
        self.parent = [-1] * n
        self.weight = [0] * n
        self.c = n

    def root(self, x: int) -> int:
        p = self.parent[x]
        if p < 0:
            return x
        r = self.root(p)
        self.weight[x] += self.weight[p]
        self.parent[x] = r
        return r

    def potential(self, x: int) -> int:
        self.root(x)
        return self.weight[x]

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def diff(self, x: int, y: int) -> int:
        assert self.same(x, y)
        return self.potential(y) - self.potential(x)

    def merge(self, x: int, y: int, w: int) -> bool:
        w += self.potential(x) - self.potential(y)
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
            w = -w
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        self.weight[y] = w
        self.c -= 1
        return True

    def size(self, x: int) -> int:
        return -self.parent[self.root(x)]

    def group_count(self) -> int:
        return self.c
