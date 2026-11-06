"""Codon port of Python/PriorityQue.py. 0-based binary heap."""

class PriorityQue[T]:
    array: list[T]
    reverse: bool

    def __init__(self, array: list[T], reverse: bool = False):
        self.array = array[:]
        self.reverse = reverse
        for i in range((len(self.array) >> 1) - 1, -1, -1):
            self._appropriate(i)

    def _higher(self, a: T, b: T) -> bool:
        return a > b if self.reverse else a < b

    def _appropriate(self, p: int):
        n = len(self.array)
        while (p << 1) + 1 < n:
            child = (p << 1) + 1
            if child + 1 < n and self._higher(self.array[child + 1], self.array[child]):
                child += 1
            if not self._higher(self.array[child], self.array[p]):
                break
            self.array[p], self.array[child] = self.array[child], self.array[p]
            p = child

    def append(self, x: T):
        self.array.append(x)
        p = len(self.array) - 1
        while p:
            q = (p - 1) >> 1
            if not self._higher(self.array[p], self.array[q]):
                break
            self.array[p], self.array[q] = self.array[q], self.array[p]
            p = q

    def pop(self):
        if not self.array:
            raise IndexError("pop from empty PriorityQue")
        res = self.array[0]
        last = self.array.pop()
        if self.array:
            self.array[0] = last
            self._appropriate(0)
        return res

    def get(self):
        if not self.array:
            raise IndexError("get from empty PriorityQue")
        return self.array[0]

    def __len__(self):
        return len(self.array)

    def __bool__(self):
        return bool(self.array)
