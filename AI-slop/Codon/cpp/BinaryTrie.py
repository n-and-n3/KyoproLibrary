class BinaryTrie:
    d: int
    world: int
    zero: list[int]
    one: list[int]
    count: list[int]

    def __init__(self, d: int):
        self.d = d
        self.world = 0
        self.zero = [-1]
        self.one = [-1]
        self.count = [0]

    def _new_node(self) -> int:
        i = len(self.count)
        self.zero.append(-1)
        self.one.append(-1)
        self.count.append(0)
        return i

    def find(self, x: int) -> bool:
        assert 0 <= x < 1 << self.d
        x ^= self.world
        i = 0
        for k in range(self.d - 1, -1, -1):
            i = self.one[i] if (x >> k) & 1 else self.zero[i]
            if i < 0:
                return False
        return self.count[i] > 0

    def insert(self, x: int):
        assert 0 <= x < 1 << self.d
        if self.find(x):
            return
        x ^= self.world
        i = 0
        self.count[i] += 1
        for k in range(self.d - 1, -1, -1):
            if (x >> k) & 1:
                j = self.one[i]
                if j < 0:
                    j = self._new_node()
                    self.one[i] = j
            else:
                j = self.zero[i]
                if j < 0:
                    j = self._new_node()
                    self.zero[i] = j
            i = j
            self.count[i] += 1

    def erase(self, x: int):
        assert 0 <= x < 1 << self.d
        if not self.find(x):
            return
        x ^= self.world
        i = 0
        self.count[i] -= 1
        for k in range(self.d - 1, -1, -1):
            i = self.one[i] if (x >> k) & 1 else self.zero[i]
            self.count[i] -= 1

    def all_xor(self, x: int):
        assert 0 <= x < 1 << self.d
        self.world ^= x

    def size(self) -> int:
        return self.count[0]

    def kth_min(self, k: int) -> int:
        assert 0 <= k < self.size()
        i = 0
        ans = 0
        for bit in range(self.d - 1, -1, -1):
            mask_bit = (self.world >> bit) & 1
            low = self.one[i] if mask_bit else self.zero[i]
            nlow = self.count[low] if low >= 0 else 0
            if k < nlow:
                i = low
            else:
                k -= nlow
                i = self.zero[i] if mask_bit else self.one[i]
                ans |= 1 << bit
        return ans

    def kth_max(self, k: int) -> int:
        return self.kth_min(self.size() - 1 - k)

    def min_xor(self, x: int) -> int:
        self.all_xor(x)
        ans = self.kth_min(0)
        self.all_xor(x)
        return ans

    def max_xor(self, x: int) -> int:
        self.all_xor(x)
        ans = self.kth_max(0)
        self.all_xor(x)
        return ans
