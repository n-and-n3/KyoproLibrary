class DynamicUnionFind[T]:
    pointer: dict[T, int]
    values: list[T]
    parent: list[int]
    c: int

    def __init__(self):
        self.pointer = dict[T, int]()
        self.values = []
        self.parent = []
        self.c = 0

    def get_pointer(self, x: T) -> int:
        if x not in self.pointer:
            self.pointer[x] = len(self.parent)
            self.values.append(x)
            self.parent.append(-1)
            self.c += 1
        return self.pointer[x]

    def _root(self, x: int) -> int:
        p = self.parent
        r = x
        while p[r] >= 0:
            r = p[r]
        while p[x] >= 0:
            y = p[x]
            p[x] = r
            x = y
        return r

    def root(self, x: T) -> T:
        return self.values[self._root(self.get_pointer(x))]

    def same(self, x: T, y: T) -> bool:
        return self._root(self.get_pointer(x)) == self._root(self.get_pointer(y))

    def size(self, x: T) -> int:
        return -self.parent[self._root(self.get_pointer(x))]

    def marge(self, x: T, y: T) -> bool:
        a = self._root(self.get_pointer(x))
        b = self._root(self.get_pointer(y))
        if a == b:
            return False
        if self.parent[a] > self.parent[b]:
            a, b = b, a
        self.parent[a] += self.parent[b]
        self.parent[b] = a
        self.c -= 1
        return True

    def group_count(self) -> int:
        return self.c

    def label(self) -> dict[T, int]:
        return {x: self._root(i) for i, x in enumerate(self.values)}

    def comped_label(self) -> dict[T, int]:
        roots = dict[int, int]()
        ans = dict[T, int]()
        for i, x in enumerate(self.values):
            r = self._root(i)
            if r not in roots:
                roots[r] = len(roots)
            ans[x] = roots[r]
        return ans

    def groups(self) -> list[list[T]]:
        d = dict[int, int]()
        ans = []
        for i, x in enumerate(self.values):
            r = self._root(i)
            if r not in d:
                d[r] = len(ans)
                ans.append([])
            ans[d[r]].append(x)
        return ans

    def group_sizes(self) -> list[int]:
        return [len(g) for g in self.groups()]
