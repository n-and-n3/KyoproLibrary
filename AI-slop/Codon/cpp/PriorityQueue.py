def _less[T](x: T, y: T) -> bool:
    return x < y


class PriorityQueue:
    data: list[T]
    comp: Callable[[T, T], bool]
    T: type = int

    def __init__(self):
        self.data = []
        self.comp = _less

    def __init__(self, comp: Callable[[T, T], bool]):
        self.data = []
        self.comp = comp

    def __init__(self, array: list[T], comp: Callable[[T, T], bool] = _less):
        self.data = array[:]
        self.comp = comp
        for i in range((len(self.data) >> 1) - 1, -1, -1):
            self._down(i)

    def _down(self, i: int):
        a = self.data
        n = len(a)
        while (i << 1) + 1 < n:
            j = (i << 1) + 1
            if j + 1 < n and self.comp(a[j + 1], a[j]):
                j += 1
            if not self.comp(a[j], a[i]):
                break
            a[i], a[j] = a[j], a[i]
            i = j

    def _up(self, i: int):
        a = self.data
        while i:
            j = (i - 1) >> 1
            if not self.comp(a[i], a[j]):
                break
            a[i], a[j] = a[j], a[i]
            i = j

    def push(self, x: T):
        self.data.append(x)
        self._up(len(self.data) - 1)

    def pop(self):
        assert self.data
        x = self.data.pop()
        if self.data:
            self.data[0] = x
            self._down(0)

    def top(self) -> T:
        assert self.data
        return self.data[0]

    def size(self) -> int:
        return len(self.data)
