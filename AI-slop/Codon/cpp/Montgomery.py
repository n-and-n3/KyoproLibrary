# cpp/Montgomery.cpp contained only a contest template. This supplies the
# intended 32-bit Montgomery arithmetic for odd moduli below 2^30.
class Montgomery:
    mod: int
    ninv: int
    r2: int

    def __init__(self, mod: int):
        assert 1 < mod < 1 << 30 and mod & 1
        self.mod = mod
        x = 1
        for _ in range(5):
            x = x * (2 - mod * x) & 0xffffffff
        self.ninv = (-x) & 0xffffffff
        r = (1 << 32) % mod
        self.r2 = r * r % mod

    def reduce(self, t: int) -> int:
        q = (t & 0xffffffff) * self.ninv & 0xffffffff
        r = (t + q * self.mod) >> 32
        return r - self.mod if r >= self.mod else r

    def encode(self, x: int) -> int:
        return self.reduce((x % self.mod) * self.r2)

    def decode(self, x: int) -> int:
        return self.reduce(x)

    def mul_mont(self, a: int, b: int) -> int:
        return self.reduce(a * b)

    def mul(self, a: int, b: int) -> int:
        return self.decode(self.mul_mont(self.encode(a), self.encode(b)))

    def pow(self, a: int, n: int) -> int:
        assert n >= 0
        a = self.encode(a)
        ans = self.encode(1)
        while n:
            if n & 1:
                ans = self.mul_mont(ans, a)
            a = self.mul_mont(a, a)
            n >>= 1
        return self.decode(ans)
