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
