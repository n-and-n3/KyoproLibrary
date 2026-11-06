class Permutation:
    N: int
    array: list[int]
    array_inv: list[int]

    def __init__(self, data):
        if isinstance(data, int):
            arr = list(range(data))
        else:
            arr = data
        n = len(arr)
        self.N = n
        self.array = arr[:]
        self.array_inv = [-1] * n
        for i, x in enumerate(arr):
            if not 0 <= x < n or self.array_inv[x] >= 0:
                raise ValueError('array is not a Permutation')
            self.array_inv[x] = i

    def pre_swap(self, i: int, j: int):
        x, y = self.array[i], self.array[j]
        self.array[i], self.array[j] = y, x
        self.array_inv[x], self.array_inv[y] = j, i

    def post_swap(self, i: int, j: int):
        x, y = self.array_inv[i], self.array_inv[j]
        self.array_inv[i], self.array_inv[j] = y, x
        self.array[x], self.array[y] = j, i

    def inverse(self):
        self.array, self.array_inv = self.array_inv, self.array

    def _step(self, forward: bool):
        a = self.array
        i = len(a) - 2
        if forward:
            while i >= 0 and a[i] >= a[i + 1]:
                i -= 1
        else:
            while i >= 0 and a[i] <= a[i + 1]:
                i -= 1
        if i >= 0:
            j = len(a) - 1
            if forward:
                while a[j] <= a[i]:
                    j -= 1
            else:
                while a[j] >= a[i]:
                    j -= 1
            a[i], a[j] = a[j], a[i]
        l, r = i + 1, len(a) - 1
        while l < r:
            a[l], a[r] = a[r], a[l]
            l += 1
            r -= 1
        for k in range(self.N):
            self.array_inv[a[k]] = k

    def next(self):
        self._step(True)

    def prev(self):
        self._step(False)

    def divided_cycles(self) -> list[list[int]]:
        seen = [False] * self.N
        ans = []
        for i in range(self.N):
            if seen[i]:
                continue
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = self.array[j]
            ans.append(cyc)
        return ans

    def p2vec(self) -> list[int]:
        return self.array[:]

    def __getitem__(self, i: int) -> int:
        return self.array[i]

    def print(self):
        print(self.array)

    def size(self) -> int:
        return self.N


def pow(P: Permutation, K: int) -> Permutation:
    ans = [0] * P.N
    for cyc in P.divided_cycles():
        n = len(cyc)
        for j in range(n):
            ans[cyc[j]] = cyc[(j + K) % n]
    return Permutation(ans)


def powpow(P: Permutation, c: int, K: int) -> Permutation:
    ans = [0] * P.N
    for cyc in P.divided_cycles():
        n = len(cyc)
        shift = 1
        base = c % n
        exp = K
        while exp:
            if exp & 1:
                shift = shift * base % n
            base = base * base % n
            exp >>= 1
        for j in range(n):
            ans[cyc[j]] = cyc[(j + shift) % n]
    return Permutation(ans)


def product(P: Permutation, Q: Permutation) -> Permutation:
    assert P.N == Q.N
    return Permutation([P.array[Q.array[i]] for i in range(P.N)])
