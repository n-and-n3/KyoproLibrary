class _UFHistory:
    parent: list[int]
    merge_times: list[int]
    time: int

    def __init__(self, n: int):
        self.parent = [-1] * n
        self.merge_times = [1 << 60] * n
        self.time = 0


class PartiallyPersistentUnionFind:
    history: _UFHistory
    cur_time: int
    is_origial: bool

    def __init__(self, n: int):
        self.history = _UFHistory(n)
        self.cur_time = 0
        self.is_origial = True

    def __init__(self, history: _UFHistory, t: int):
        self.history = history
        self.cur_time = t
        self.is_origial = False

    def _root_at(self, x: int, t: int) -> int:
        h = self.history
        while h.merge_times[x] <= t:
            x = h.parent[x]
        return x

    def root(self, x: int) -> int:
        return self._root_at(x, self.cur_time)

    def same(self, x: int, y: int) -> bool:
        return self.root(x) == self.root(y)

    def merge(self, x: int, y: int) -> bool:
        assert self.is_origial
        h = self.history
        h.time += 1
        self.cur_time = h.time
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        if h.parent[x] > h.parent[y]:
            x, y = y, x
        h.parent[x] += h.parent[y]
        h.parent[y] = x
        h.merge_times[y] = h.time
        return True

    def size(self, v: int) -> int:
        assert self.is_origial
        return -self.history.parent[self.root(v)]

    def connect_time(self, x: int, y: int) -> int:
        h = self.history
        if self._root_at(x, h.time) != self._root_at(y, h.time):
            return -1
        lo, hi = 0, h.time
        while lo < hi:
            mid = (lo + hi) >> 1
            if self._root_at(x, mid) == self._root_at(y, mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def copy(self) -> PartiallyPersistentUnionFind:
        return PartiallyPersistentUnionFind(self.history, self.cur_time)

    def print(self):
        print(self.history.parent)
        print(self.history.merge_times)
