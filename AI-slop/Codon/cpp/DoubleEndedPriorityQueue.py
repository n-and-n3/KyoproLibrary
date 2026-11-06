class DoubleEndedPriorityQueue:
    min_data: list[T]
    max_data: list[T]
    count: dict[T, int]
    n: int
    T: type = int

    def __init__(self):
        self.min_data = list[T]()
        self.max_data = list[T]()
        self.count = dict[T, int]()
        self.n = 0

    def __init__(self, array: list[T]):
        self.min_data = []
        self.max_data = []
        self.count = dict[T, int]()
        self.n = 0
        for x in array:
            self.push(x)

    def _push(self, a: list[T], x: T, is_min: bool):
        a.append(x)
        i = len(a) - 1
        while i:
            j = (i - 1) >> 1
            if (a[i] < a[j]) == is_min and a[i] != a[j]:
                a[i], a[j] = a[j], a[i]
                i = j
            else:
                break

    def _pop(self, a: list[T], is_min: bool):
        x = a.pop()
        if not a:
            return
        a[0] = x
        n = len(a)
        i = 0
        while (i << 1) + 1 < n:
            j = (i << 1) + 1
            if j + 1 < n and (a[j + 1] < a[j]) == is_min and a[j + 1] != a[j]:
                j += 1
            if (a[j] < a[i]) == is_min and a[j] != a[i]:
                a[i], a[j] = a[j], a[i]
                i = j
            else:
                break

    def _clean(self, a: list[T], is_min: bool):
        while a and self.count.get(a[0], 0) == 0:
            self._pop(a, is_min)

    def push(self, x: T):
        self.count[x] = self.count.get(x, 0) + 1
        self.n += 1
        self._push(self.min_data, x, True)
        self._push(self.max_data, x, False)

    def get_min(self) -> T:
        self._clean(self.min_data, True)
        assert self.n > 0
        return self.min_data[0]

    def get_max(self) -> T:
        self._clean(self.max_data, False)
        assert self.n > 0
        return self.max_data[0]

    def pop_min(self):
        x = self.get_min()
        self.count[x] -= 1
        self.n -= 1
        self._pop(self.min_data, True)

    def pop_max(self):
        x = self.get_max()
        self.count[x] -= 1
        self.n -= 1
        self._pop(self.max_data, False)

    def size(self) -> int:
        return self.n
