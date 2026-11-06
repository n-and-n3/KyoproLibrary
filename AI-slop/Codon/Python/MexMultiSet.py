"""Codon port of Python/MexMultiSet.py."""

import heapq as hq

class MexMultiSet:
    L = 10000
    mulS: dict[int, int]
    q: list[int]
    inf: int
    length: int

    def __init__(self, array: list[int]):
        self.mulS = dict[int, int]()
        for x in array:
            self.mulS[x] = self.mulS.get(x, 0) + 1
        self.q = [i for i in range(MexMultiSet.L) if self.mulS.get(i, 0) == 0]
        self.q.append(MexMultiSet.L)
        hq.heapify(self.q)
        self.inf = MexMultiSet.L
        self.length = len(array)

    def add(self, x: int) -> None:
        self.mulS[x] = self.mulS.get(x, 0) + 1
        self.length += 1

    def remove(self, x: int) -> None:
        count = self.mulS.get(x, 0)
        if count == 0:
            raise KeyError(str(x))
        self.mulS[x] = count - 1
        self.length -= 1
        if x >= 0 and x < self.inf and count == 1:
            hq.heappush(self.q, x)

    def discard(self, x: int) -> None:
        if self.mulS.get(x, 0):
            self.remove(x)

    def mex(self) -> int:
        while True:
            x = self.q[0]
            if x == self.inf:
                hq.heappop(self.q)
                for i in range(self.inf, self.inf + MexMultiSet.L):
                    if self.mulS.get(i, 0) == 0:
                        hq.heappush(self.q, i)
                self.inf += MexMultiSet.L
                hq.heappush(self.q, self.inf)
            elif self.mulS.get(x, 0):
                hq.heappop(self.q)
            else:
                return x

    def __len__(self) -> int:
        return self.length

    def __contains__(self, x: int) -> bool:
        return self.mulS.get(x, 0) > 0
