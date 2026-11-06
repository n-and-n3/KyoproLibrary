class _ArrayHistory[T]:
    historys: list[list[tuple[int, T]]]
    version: int

    def __init__(self, array: list[T]):
        self.historys = [[(0, x)] for x in array]
        self.version = 0


class PartiallyPersistentArray[T]:
    data: _ArrayHistory[T]
    version: int
    is_original: bool
    sz: int

    def __init__(self, array: list[T]):
        self.data = _ArrayHistory(array)
        self.version = 0
        self.is_original = True
        self.sz = len(array)

    def __init__(self, n: int, initial: T = 0):
        self.data = _ArrayHistory([initial] * n)
        self.version = 0
        self.is_original = True
        self.sz = n

    def __init__(self, history: _ArrayHistory[T], version: int):
        self.data = history
        self.version = version
        self.is_original = False
        self.sz = len(history.historys)

    def get(self, ind: int) -> T:
        assert 0 <= ind < self.sz
        hist = self.data.historys[ind]
        if self.is_original:
            return hist[-1][1]
        lo, hi = 0, len(hist)
        while hi - lo > 1:
            mid = (lo + hi) >> 1
            if hist[mid][0] <= self.version:
                lo = mid
            else:
                hi = mid
        return hist[lo][1]

    def __getitem__(self, ind: int) -> T:
        return self.get(ind)

    def write(self, ind: int, x: T):
        assert self.is_original and 0 <= ind < self.sz
        self.data.version += 1
        self.version = self.data.version
        hist = self.data.historys[ind]
        if hist[-1][1] != x:
            hist.append((self.version, x))

    def __setitem__(self, ind: int, x: T):
        self.write(ind, x)

    def size(self) -> int:
        return self.sz

    def copy(self) -> PartiallyPersistentArray[T]:
        version = self.data.version if self.is_original else self.version
        return PartiallyPersistentArray(self.data, version)

    def to_list(self) -> list[T]:
        return [self.get(i) for i in range(self.sz)]


class PartiallyPersistentUnionFind:
    parent: PartiallyPersistentArray[int]
    c: int
    is_original: bool

    def __init__(self, n: int):
        self.parent = PartiallyPersistentArray(n, -1)
        self.c = n
        self.is_original = True

    def __init__(self, parent: PartiallyPersistentArray[int], c: int):
        self.parent = parent.copy()
        self.c = c
        self.is_original = False

    def root(self, x: int) -> int:
        p = self.parent
        r = x
        while p[r] >= 0:
            r = p[r]
        if self.is_original:
            while p[x] >= 0:
                y = p[x]
                p[x] = r
                x = y
        return r

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def size(self, x: int) -> int:
        return -self.parent[self.root(x)]

    def merge(self, x: int, y: int) -> bool:
        assert self.is_original
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        p = self.parent
        if p[x] > p[y]:
            x, y = y, x
        p[x] = p[x] + p[y]
        p[y] = x
        self.c -= 1
        return True

    def group_count(self) -> int:
        return self.c

    def copy(self) -> PartiallyPersistentUnionFind:
        return PartiallyPersistentUnionFind(self.parent, self.c)

    def label(self) -> list[int]:
        n = self.parent.sz
        return [self.root(i) for i in range(n)]

    def comped_label(self) -> list[int]:
        roots = dict[int, int]()
        ans = []
        for r in self.label():
            if r not in roots:
                roots[r] = len(roots)
            ans.append(roots[r])
        return ans

    def groups(self) -> list[list[int]]:
        lab = self.comped_label()
        ans = [[] for _ in range(self.c)]
        for i, j in enumerate(lab):
            ans[j].append(i)
        return ans

    def group_sizes(self) -> list[int]:
        return [len(g) for g in self.groups()]

    def print(self):
        print(self.parent.to_list())
