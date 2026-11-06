class UnionFind:
    parent: list[int]
    next_v: list[int]
    c: int

    def __init__(self, n: int):
        self.parent = [-1] * n
        self.next_v = list(range(n))
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
        p = self.parent
        if p[x] > p[y]:
            x, y = y, x
        p[x] += p[y]
        p[y] = x
        self.next_v[x], self.next_v[y] = self.next_v[y], self.next_v[x]
        self.c -= 1
        return True

    def group_count(self) -> int:
        return self.c

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
        for i in range(len(ans)):
            if ans[i] >= 0:
                continue
            x = i
            while ans[x] < 0:
                ans[x] = c
                x = self.next_v[x]
            c += 1
        return ans

    def comped_label(self) -> list[int]:
        return self.label()

    def groups(self) -> list[list[int]]:
        ans = []
        seen = [False] * len(self.parent)
        for i in range(len(seen)):
            if not seen[i]:
                g = self.component(i)
                for x in g:
                    seen[x] = True
                ans.append(g)
        return ans

    def group_sizes(self) -> list[int]:
        return [len(g) for g in self.groups()]

    def push(self):
        self.parent.append(-1)
        self.next_v.append(len(self.next_v))
        self.c += 1

    def print(self):
        print(self.groups())
