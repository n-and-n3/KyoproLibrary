class UnionFindwithMonoid[T, U]:
    parent: list[int]
    next_v: list[int]
    data: list[T]
    op: Callable[[T, T], T]
    e: Callable[[], T]
    global_op: Callable[[T, T, U], U]
    global_value: U
    c: int

    def __init__(self, n: int, data: list[T], op: Callable[[T, T], T], e: Callable[[], T], global_op: Callable[[T, T, U], U], global_value: U):
        assert n == len(data)
        self.parent = [-1] * n
        self.next_v = list(range(n))
        self.data = data[:]
        self.op = op
        self.e = e
        self.global_op = global_op
        self.global_value = global_value
        self.c = n

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

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def size(self, x: int) -> int:
        return -self.parent[self.root(x)]

    def merge(self, x: int, y: int) -> bool:
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.global_value = self.global_op(self.data[x], self.data[y], self.global_value)
        self.data[x] = self.op(self.data[x], self.data[y])
        self.data[y] = self.e()
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        self.next_v[x], self.next_v[y] = self.next_v[y], self.next_v[x]
        self.c -= 1
        return True

    def group_count(self) -> int:
        return self.c

    def get_global_value(self) -> U:
        return self.global_value

    def get_component_value(self, x: int) -> T:
        return self.data[self.root(x)]

    def component(self, v: int) -> list[int]:
        ans = [v]
        x = self.next_v[v]
        while x != v:
            ans.append(x)
            x = self.next_v[x]
        return ans

    def label(self) -> list[int]:
        ans = [-1] * len(self.parent)
        c = 0
        for v in range(len(ans)):
            if ans[v] >= 0:
                continue
            x = v
            while ans[x] < 0:
                ans[x] = c
                x = self.next_v[x]
            c += 1
        return ans

    def groups(self) -> list[list[int]]:
        ans = [[] for _ in range(self.c)]
        lab = self.label()
        for i in range(len(lab)):
            ans[lab[i]].append(i)
        return ans

    def group_sizes(self) -> list[int]:
        return [len(g) for g in self.groups()]
