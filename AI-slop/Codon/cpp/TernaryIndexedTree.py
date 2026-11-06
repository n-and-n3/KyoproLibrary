class TIT[T]:
    array: list[T]
    sz: int

    def __init__(self, data: list[T]):
        self.sz = 1
        while self.sz < len(data):
            self.sz = 3 * self.sz + 1
        self.array = [T(0)] * (self.sz + 1)
        for i, x in enumerate(data):
            self.array[i + 1] += x
        for i in range(1, self.sz + 1):
            j = i + (i & -i)
            if j <= self.sz:
                self.array[j] += self.array[i]

    def cum(self, ind: int) -> T:
        res = T(0)
        while ind > 0:
            res += self.array[ind]
            ind -= ind & -ind
        return res

    def get(self, ind: int) -> T:
        return self.cum(ind) - self.cum(ind - 1)

    def add(self, ind: int, x: T):
        while ind <= self.sz:
            self.array[ind] += x
            ind += ind & -ind

    def write(self, ind: int, x: T):
        self.add(ind, x - self.get(ind))

    def size(self) -> int:
        return self.sz
