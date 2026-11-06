class BinaryTreeSet:
    sz: int
    cap: int
    array: list[bool]

    def __init__(self, universe: int):
        self.sz = universe
        self.cap = 1
        while self.cap < self.sz:
            self.cap <<= 1
        self.array = [False] * (2 * self.cap)

    def __init__(self, bitarray: str):
        self.sz = len(bitarray)
        self.cap = 1
        while self.cap < self.sz:
            self.cap <<= 1
        self.array = [False] * (2 * self.cap)
        for i in range(self.sz):
            self.array[self.cap + i] = bitarray[i] != '0'
        for i in range(self.cap - 1, 0, -1):
            self.array[i] = self.array[i << 1] or self.array[i << 1 | 1]

    def contains(self, x: int) -> bool:
        return self.array[self.cap + x]

    def write(self, i: int, x: bool):
        i += self.cap
        self.array[i] = x
        while i > 1:
            i >>= 1
            self.array[i] = self.array[i << 1] or self.array[i << 1 | 1]

    def insert(self, i: int):
        self.write(i, True)

    def erase(self, i: int):
        self.write(i, False)

    def flip(self, i: int):
        self.write(i, not self.contains(i))

    def predecessor(self, i: int) -> int:
        if i < 0 or self.sz == 0:
            return -1
        i = min(i, self.sz - 1) + self.cap
        if not self.array[i]:
            while i > 1:
                if i & 1 and self.array[i - 1]:
                    i -= 1
                    break
                i >>= 1
            else:
                return -1
        while i < self.cap:
            i = i << 1 | int(self.array[i << 1 | 1])
        return i - self.cap

    def successor(self, i: int) -> int:
        if i >= self.sz or self.sz == 0:
            return -1
        i = max(i, 0) + self.cap
        if not self.array[i]:
            while i > 1:
                if (i & 1) == 0 and self.array[i + 1]:
                    i += 1
                    break
                i >>= 1
            else:
                return -1
        while i < self.cap:
            i = i << 1 | int(not self.array[i << 1])
        x = i - self.cap
        return x if x < self.sz else -1
