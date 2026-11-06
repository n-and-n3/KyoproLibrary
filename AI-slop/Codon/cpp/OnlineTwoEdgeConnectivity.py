_INF_TIME = 1 << 60


class _ComponentForest:
    parent: list[int]
    parent_time: list[int]
    next_v: list[int]
    current_parent: list[int]
    events: list[list[tuple[int, int, int]]]

    def __init__(self, n: int):
        self.parent = [-1] * n
        self.parent_time = [_INF_TIME] * n
        self.next_v = list(range(n))
        self.current_parent = [-1] * n
        self.events = [[] for _ in range(n)]

    def root(self, v: int) -> int:
        p = self.current_parent
        r = v
        while p[r] >= 0:
            r = p[r]
        while p[v] >= 0:
            nxt = p[v]
            p[v] = r
            v = nxt
        return r

    def root_at(self, v: int, t: int) -> int:
        while self.parent_time[v] <= t:
            v = self.parent[v]
        return v

    def root_size(self, r: int) -> int:
        return -self.current_parent[r]

    def block_count(self, r: int) -> int:
        return self.events[r][-1][2] if self.events[r] else 1

    def attach(self, big: int, small: int, t: int):
        self.current_parent[big] += self.current_parent[small]
        self.parent[small] = big
        self.parent_time[small] = t
        self.current_parent[small] = big

    def splice(self, a: int, b: int):
        self.next_v[a], self.next_v[b] = self.next_v[b], self.next_v[a]

    def record(self, r: int, t: int, blocks: int = 0):
        self.events[r].append((t, self.root_size(r), blocks))

    def state_at(self, v: int, t: int) -> tuple[int, int]:
        r = self.root_at(v, t)
        ev = self.events[r]
        lo, hi = 0, len(ev)
        while lo < hi:
            mid = (lo + hi) >> 1
            if ev[mid][0] <= t:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return (1, 1)
        return (ev[lo - 1][1], ev[lo - 1][2])

    def first_same_time(self, a: int, b: int) -> int:
        answer = 0
        while a != b:
            if self.parent_time[a] > self.parent_time[b]:
                a, b = b, a
            t = self.parent_time[a]
            if t == _INF_TIME:
                return -1
            answer = t
            a = self.parent[a]
        return answer

    def first_size_time(self, v: int, need: int, current_time: int) -> int:
        if need <= 1:
            return 0
        if self.state_at(v, current_time)[0] < need:
            return -1
        lo, hi = 0, current_time
        while lo < hi:
            mid = (lo + hi) >> 1
            if self.state_at(v, mid)[0] >= need:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def members(self, v: int) -> list[int]:
        ans = [v]
        x = self.next_v[v]
        while x != v:
            ans.append(x)
            x = self.next_v[x]
        return ans

    def groups(self) -> list[list[int]]:
        ans = []
        for i in range(len(self.parent)):
            if self.parent[i] < 0:
                ans.append(self.members(i))
        return ans


class OnlineTwoEdgeConnectivity:
    n_: int
    time_: int
    cc_count_: int
    ecc_count_: int
    cc_: _ComponentForest
    ecc_: _ComponentForest
    bridge_parent_: list[int]
    visit_time_: list[int]
    count_history_: list[tuple[int, int]]

    def __init__(self, n: int, expected_additions: int = 0):
        assert n >= 0
        self.n_ = n
        self.time_ = 0
        self.cc_count_ = n
        self.ecc_count_ = n
        self.cc_ = _ComponentForest(n)
        self.ecc_ = _ComponentForest(n)
        self.bridge_parent_ = [-1] * n
        self.visit_time_ = [0] * n
        self.count_history_ = [(n, n)]

    def time(self) -> int:
        return self.time_

    def reserve_additions(self, expected_total_additions: int):
        assert expected_total_additions >= self.time_

    def _bridge_parent(self, r: int) -> int:
        p = self.bridge_parent_[r]
        if p < 0:
            return -1
        p = self.ecc_.root(p)
        self.bridge_parent_[r] = p
        return p

    def _reroot(self, r: int):
        child = -1
        while r >= 0:
            parent = self._bridge_parent(r)
            self.bridge_parent_[r] = child
            child = r
            r = parent

    def _collect_path(self, a: int, b: int, pa: int, pb: int) -> tuple[list[int], list[int], int]:
        path_a = [a]
        path_b = [b]
        self.visit_time_[a] = self.time_
        self.visit_time_[b] = self.time_
        a, b = pa, pb
        lca = -1
        while lca < 0:
            if a >= 0:
                path_a.append(a)
                if self.visit_time_[a] == self.time_:
                    lca = a
                    break
                self.visit_time_[a] = self.time_
                a = self._bridge_parent(a)
            if b >= 0:
                path_b.append(b)
                if self.visit_time_[b] == self.time_:
                    lca = b
                    break
                self.visit_time_[b] = self.time_
                b = self._bridge_parent(b)
        while path_a[-1] != lca:
            path_a.pop()
        while path_b[-1] != lca:
            path_b.pop()
        path_b.pop()
        return path_a, path_b, lca

    def _finish_merge(self, big: int, parent_above: int, cc_root: int, removed: int):
        self.ecc_.record(big, self.time_)
        self.bridge_parent_[big] = parent_above
        self.ecc_count_ -= removed
        self.cc_.record(cc_root, self.time_, self.cc_.block_count(cc_root) - removed)

    def _merge_adjacent(self, a: int, b: int, parent_above: int, cc_root: int):
        if self.ecc_.root_size(a) < self.ecc_.root_size(b):
            a, b = b, a
        self.ecc_.attach(a, b, self.time_)
        self.ecc_.splice(a, b)
        self._finish_merge(a, parent_above, cc_root, 1)

    def _merge_path(self, a: int, b: int, cc_root: int):
        pa = self._bridge_parent(a)
        if pa == b:
            self._merge_adjacent(a, b, self._bridge_parent(b), cc_root)
            return
        pb = self._bridge_parent(b)
        if pb == a:
            self._merge_adjacent(a, b, pa, cc_root)
            return
        path_a, path_b, lca = self._collect_path(a, b, pa, pb)
        parent_above = self._bridge_parent(lca)
        big = path_a[0]
        for r in path_a:
            if self.ecc_.root_size(r) > self.ecc_.root_size(big):
                big = r
        for r in path_b:
            if self.ecc_.root_size(r) > self.ecc_.root_size(big):
                big = r
        for r in path_a:
            if r != big:
                self.ecc_.attach(big, r, self.time_)
                self.ecc_.splice(big, r)
        for r in path_b:
            if r != big:
                self.ecc_.attach(big, r, self.time_)
                self.ecc_.splice(big, r)
        self._finish_merge(big, parent_above, cc_root, len(path_a) + len(path_b) - 1)

    def add_edge(self, u: int, v: int):
        assert 0 <= u < self.n_ and 0 <= v < self.n_
        self.time_ += 1
        if u != v:
            a = self.ecc_.root(u)
            b = self.ecc_.root(v)
            if a != b:
                ca = self.cc_.root(u)
                cb = self.cc_.root(v)
                if ca != cb:
                    if self.cc_.root_size(ca) < self.cc_.root_size(cb):
                        ca, cb = cb, ca
                        a, b = b, a
                    blocks = self.cc_.block_count(ca) + self.cc_.block_count(cb)
                    self._reroot(b)
                    self.bridge_parent_[b] = a
                    self.cc_.attach(ca, cb, self.time_)
                    self.cc_.splice(a, b)
                    self.cc_.record(ca, self.time_, blocks)
                    self.cc_count_ -= 1
                else:
                    self._merge_path(a, b, ca)
        self.count_history_.append((self.cc_count_, self.ecc_count_))

    def query(self, a: int, b: int, t: int = -1) -> int:
        if t < 0:
            if self.ecc_.root(a) == self.ecc_.root(b):
                return 2
            return 1 if self.cc_.root(a) == self.cc_.root(b) else 0
        assert t <= self.time_
        if self.cc_.root_at(a, t) != self.cc_.root_at(b, t):
            return 0
        return 2 if self.ecc_.root_at(a, t) == self.ecc_.root_at(b, t) else 1

    def connected_component_size(self, v: int, t: int = -1) -> int:
        return self.cc_.root_size(self.cc_.root(v)) if t < 0 else self.cc_.state_at(v, t)[0]

    def two_edge_connected_component_size(self, v: int, t: int = -1) -> int:
        return self.ecc_.root_size(self.ecc_.root(v)) if t < 0 else self.ecc_.state_at(v, t)[0]

    def connected_component_count(self, t: int = -1) -> int:
        return self.cc_count_ if t < 0 else self.count_history_[t][0]

    def two_edge_connected_component_count(self, t: int = -1) -> int:
        return self.ecc_count_ if t < 0 else self.count_history_[t][1]

    def two_edge_connected_component_count_in_connected_component(self, v: int, t: int = -1) -> int:
        r = self.cc_.root(v)
        return self.cc_.block_count(r) if t < 0 else self.cc_.state_at(v, t)[1]

    def first_connected_time(self, a: int, b: int) -> int:
        return self.cc_.first_same_time(a, b)

    def first_two_edge_connected_time(self, a: int, b: int) -> int:
        return self.ecc_.first_same_time(a, b)

    def first_connected_component_size_at_least_time(self, v: int, need: int) -> int:
        return self.cc_.first_size_time(v, need, self.time_)

    def first_two_edge_connected_component_size_at_least_time(self, v: int, need: int) -> int:
        return self.ecc_.first_size_time(v, need, self.time_)

    def connected_component_vertices(self, v: int) -> list[int]:
        return self.cc_.members(v)

    def two_edge_connected_component_vertices(self, v: int) -> list[int]:
        return self.ecc_.members(v)

    def connected_components(self) -> list[list[int]]:
        return self.cc_.groups()

    def two_edge_connected_components(self) -> list[list[int]]:
        return self.ecc_.groups()
