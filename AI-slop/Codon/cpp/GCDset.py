from math import gcd


class GCDset:
    cap: int
    leaf_count: int
    active_size: int
    tree: list[int]
    pos_map: dict[int, int]

    def __init__(self):
        self.cap = 4
        self.leaf_count = 0
        self.active_size = 0
        self.tree = [0] * 8
        self.pos_map = dict[int, int]()

    def _update(self, i: int, x: int):
        i += self.cap
        self.tree[i] = x
        while i > 1:
            i >>= 1
            self.tree[i] = gcd(self.tree[i << 1], self.tree[i << 1 | 1])

    def _rebuild(self):
        vals = [self.tree[self.cap + i] for i in range(self.leaf_count) if self.tree[self.cap + i] != 0]
        cap = 4
        while cap <= 2 * len(vals):
            cap <<= 1
        self.cap = cap
        self.tree = [0] * (2 * cap)
        self.pos_map = dict[int, int]()
        self.leaf_count = 0
        for x in vals:
            self.pos_map[x] = self.leaf_count
            self.tree[cap + self.leaf_count] = x
            self.leaf_count += 1
        for i in range(cap - 1, 0, -1):
            self.tree[i] = gcd(self.tree[i << 1], self.tree[i << 1 | 1])

    def insert(self, x: int):
        if x in self.pos_map:
            return
        if self.leaf_count == self.cap:
            self._rebuild()
        self.pos_map[x] = self.leaf_count
        self._update(self.leaf_count, x)
        self.leaf_count += 1
        self.active_size += 1

    def erase(self, x: int):
        if x not in self.pos_map:
            raise ValueError('element does not exist')
        self._update(self.pos_map.pop(x), 0)
        self.active_size -= 1

    def contains(self, x: int) -> bool:
        return x in self.pos_map

    def size(self) -> int:
        return self.active_size

    def get_gcd(self) -> int:
        return self.tree[1]


class GCDmultiset:
    cap: int
    leaf_count: int
    active_size: int
    tree: list[int]
    prev_idx: list[int]
    head_map: dict[int, int]

    def __init__(self):
        self.cap = 4
        self.leaf_count = 0
        self.active_size = 0
        self.tree = [0] * 8
        self.prev_idx = [-1] * 4
        self.head_map = dict[int, int]()

    def _update(self, i: int, x: int):
        i += self.cap
        self.tree[i] = x
        while i > 1:
            i >>= 1
            self.tree[i] = gcd(self.tree[i << 1], self.tree[i << 1 | 1])

    def _rebuild(self):
        vals = [self.tree[self.cap + i] for i in range(self.leaf_count) if self.tree[self.cap + i] != 0]
        cap = 4
        while cap <= 2 * len(vals):
            cap <<= 1
        self.cap = cap
        self.tree = [0] * (2 * cap)
        self.prev_idx = [-1] * cap
        self.head_map = dict[int, int]()
        self.leaf_count = 0
        for x in vals:
            i = self.leaf_count
            self.leaf_count += 1
            self.prev_idx[i] = self.head_map.get(x, -1)
            self.head_map[x] = i
            self.tree[cap + i] = x
        for i in range(cap - 1, 0, -1):
            self.tree[i] = gcd(self.tree[i << 1], self.tree[i << 1 | 1])

    def insert(self, x: int):
        if self.leaf_count == self.cap:
            self._rebuild()
        i = self.leaf_count
        self.leaf_count += 1
        self.prev_idx[i] = self.head_map.get(x, -1)
        self.head_map[x] = i
        self._update(i, x)
        self.active_size += 1

    def erase(self, x: int):
        if x not in self.head_map:
            raise ValueError('element does not exist')
        i = self.head_map[x]
        j = self.prev_idx[i]
        if j < 0:
            self.head_map.pop(x)
        else:
            self.head_map[x] = j
        self._update(i, 0)
        self.active_size -= 1

    def contains(self, x: int) -> bool:
        return x in self.head_map

    def size(self) -> int:
        return self.active_size

    def get_gcd(self) -> int:
        return self.tree[1]
