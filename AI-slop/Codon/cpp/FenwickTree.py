class BIT:
    array: list[T]
    N: int
    T: type = int

    def __init__(self, N: int):
        self.N = N
        self.array = [T(0)] * (N + 1)

    def __init__(self, data: list[T]):
        self.N = len(data)
        self.array = [T(0)] * (self.N + 1)
        for i in range(self.N):
            self.array[i + 1] += data[i]
            j = i + 1 + ((i + 1) & (-i - 1))
            if j <= self.N:
                self.array[j] += self.array[i + 1]

    def add(self, ind: int, x: T):
        while ind <= self.N:
            self.array[ind] += x
            ind += ind & -ind

    def sum(self, ind: int) -> T:
        res = T(0)
        while ind > 0:
            res += self.array[ind]
            ind -= ind & -ind
        return res
