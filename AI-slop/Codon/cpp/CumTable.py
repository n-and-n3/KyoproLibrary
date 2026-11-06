class CumulativeTable[T]:
    array_sum: list[T]

    def __init__(self, array: list[T]):
        self.array_sum = [T(0)]
        for x in array:
            self.array_sum.append(self.array_sum[-1] + x)

    def prod(self, l: int, r: int) -> T:
        return self.array_sum[r] - self.array_sum[l]
