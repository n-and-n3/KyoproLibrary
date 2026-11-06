"""Codon port of Python/DeletablePriorityQue.py."""

class DeletablePriorityQue[T]:
    array: list[T]
    reverse: bool
    maltiset: dict[T, int]
    length: int

    def __init__(self, array: list[T], reverse: bool = False):
        self.array = array[:]
        self.reverse = reverse
        self.maltiset = dict[T, int]()
        self.length = len(array)
        for x in array:
            self.maltiset[x] = self.maltiset.get(x, 0) + 1
        for i in range((len(self.array) >> 1) - 1, -1, -1):
            self._appropriate(i)

    def _higher(self, a: T, b: T) -> bool:
        return a > b if self.reverse else a < b

    def _appropriate(self, p: int) -> None:
        n = len(self.array)
        while (p << 1) + 1 < n:
            child = (p << 1) + 1
            if child + 1 < n and self._higher(self.array[child + 1], self.array[child]):
                child += 1
            if not self._higher(self.array[child], self.array[p]):
                break
            self.array[p], self.array[child] = self.array[child], self.array[p]
            p = child

    def _clean(self) -> None:
        while self.array and self.maltiset.get(self.array[0], 0) == 0:
            last = self.array.pop()
            if self.array:
                self.array[0] = last
                self._appropriate(0)

    def append(self, x: T) -> None:
        self.maltiset[x] = self.maltiset.get(x, 0) + 1
        self.length += 1
        self.array.append(x)
        p = len(self.array) - 1
        while p:
            q = (p - 1) >> 1
            if not self._higher(self.array[p], self.array[q]):
                break
            self.array[p], self.array[q] = self.array[q], self.array[p]
            p = q

    def remove(self, x: T) -> None:
        count = self.maltiset.get(x, 0)
        if count == 0:
            raise KeyError(str(x))
        self.maltiset[x] = count - 1
        self.length -= 1
        self._clean()

    def discard(self, x: T) -> None:
        if self.maltiset.get(x, 0):
            self.remove(x)

    def pop(self) -> T:
        x = self.get()
        self.remove(x)
        return x

    def get(self) -> T:
        self._clean()
        if not self.array:
            raise IndexError("get from empty DeletablePriorityQue")
        return self.array[0]

    def __len__(self) -> int:
        return self.length

    def __bool__(self) -> bool:
        return self.length != 0
