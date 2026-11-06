class Eratosthenes:
    isprime: list[bool]
    minfactor: list[int]
    mobius: list[int]

    def __init__(self, N: int):
        self.isprime = [False] * (N + 1)
        self.minfactor = [-1] * (N + 1)
        self.mobius = [1] * (N + 1)
        if N >= 1:
            self.minfactor[1] = 1
        primes = []
        for i in range(2, N + 1):
            if self.minfactor[i] < 0:
                self.minfactor[i] = i
                self.isprime[i] = True
                self.mobius[i] = -1
                primes.append(i)
            for p in primes:
                x = i * p
                if x > N:
                    break
                self.minfactor[x] = p
                if i % p == 0:
                    self.mobius[x] = 0
                    break
                self.mobius[x] = -self.mobius[i]

    def factorize(self, n: int) -> list[tuple[int, int]]:
        ans = []
        while n > 1:
            p = self.minfactor[n]
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            ans.append((p, e))
        return ans

    def divisors(self, n: int) -> list[int]:
        ans = [1]
        for p, e in self.factorize(n):
            size = len(ans)
            power = 1
            for _ in range(e):
                power *= p
                for i in range(size):
                    ans.append(ans[i] * power)
        ans.sort()
        return ans


def fast_zeta(f: list[int]):
    n = len(f)
    er = Eratosthenes(n - 1)
    for p in range(2, n):
        if er.isprime[p]:
            for k in range((n - 1) // p, 0, -1):
                f[k] += f[k * p]


def fast_mobius(f: list[int]):
    n = len(f)
    er = Eratosthenes(n - 1)
    for p in range(2, n):
        if er.isprime[p]:
            for k in range(1, (n - 1) // p + 1):
                f[k] -= f[k * p]


def Eular_func(N: int) -> list[int]:
    ans = list(range(N + 1))
    for p in range(2, N + 1):
        if ans[p] == p:
            for j in range(p, N + 1, p):
                ans[j] = ans[j] // p * (p - 1)
    return ans


def _round_div(x: int, d: int) -> int:
    return (x + d // 2) // d if x >= 0 else -((-x + d // 2) // d)


class Gauss_Int:
    re: int
    im: int

    def __init__(self, re: int = 0, im: int = 0):
        self.re = re
        self.im = im

    def __add__(self, other: Gauss_Int) -> Gauss_Int:
        return Gauss_Int(self.re + other.re, self.im + other.im)

    def __sub__(self, other: Gauss_Int) -> Gauss_Int:
        return Gauss_Int(self.re - other.re, self.im - other.im)

    def __mul__(self, other: Gauss_Int) -> Gauss_Int:
        return Gauss_Int(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

    def __truediv__(self, other: Gauss_Int) -> Gauss_Int:
        d = other.abs()
        return Gauss_Int(_round_div(self.re * other.re + self.im * other.im, d), _round_div(self.im * other.re - self.re * other.im, d))

    def __mod__(self, other: Gauss_Int) -> Gauss_Int:
        return self - other * (self / other)

    def abs(self) -> int:
        return self.re * self.re + self.im * self.im


def gcd(a: Gauss_Int, b: Gauss_Int) -> Gauss_Int:
    while b.abs() != 0:
        a, b = b, a % b
    return a
