import random

_MOD = (1 << 61) - 1
_BASE = random.randrange(1 << 30, _MOD - 1)


def _mul(a: int, b: int) -> int:
    au, ad = a >> 31, a & ((1 << 31) - 1)
    bu, bd = b >> 31, b & ((1 << 31) - 1)
    mid = ad * bu + au * bd
    x = au * bu * 2 + (mid >> 30) + ((mid & ((1 << 30) - 1)) << 31) + ad * bd
    x = (x >> 61) + (x & _MOD)
    return x - _MOD if x >= _MOD else x


class RollingHashEngine:
    root: int
    MOD: int
    base: int

    def __init__(self, bound: int = 1 << 30):
        self.root = 37
        self.MOD = _MOD
        self.base = _BASE

    def Mul(self, a: int, b: int) -> int:
        return _mul(a, b)

    def CalcMod(self, x: int) -> int:
        x = (x >> 61) + (x & _MOD)
        return x - _MOD if x >= _MOD else x

    def Pow(self, a: int, n: int) -> int:
        res = 1
        while n:
            if n & 1:
                res = _mul(res, a)
            a = _mul(a, a)
            n >>= 1
        return res

    def get_base(self, bound: int) -> int:
        return _BASE


class RollingHash:
    data: list[int]
    pows: list[int]
    base: int
    sz: int

    def __init__(self, s: str):
        self.sz = len(s)
        self.base = _BASE
        self.data = [0] * (self.sz + 1)
        self.pows = [1] * (self.sz + 1)
        for i in range(self.sz):
            self.data[i + 1] = (_mul(self.data[i], self.base) + ord(s[i])) % _MOD
            self.pows[i + 1] = _mul(self.pows[i], self.base)

    def get(self, l: int, r: int) -> int:
        assert 0 <= l <= r <= self.sz
        x = self.data[r] - _mul(self.data[l], self.pows[r - l])
        return x + _MOD if x < 0 else x

    def get_all(self) -> int:
        return self.data[self.sz]

    def concat(self, a: int, b: int, c: int, d: int) -> int:
        return (_mul(self.get(a, b), self._pow(d - c)) + self.get(c, d)) % _MOD

    def _pow(self, n: int) -> int:
        return self.pows[n] if n <= self.sz else self._power(self.base, n)

    def _power(self, a: int, n: int) -> int:
        ans = 1
        while n:
            if n & 1:
                ans = _mul(ans, a)
            a = _mul(a, a)
            n >>= 1
        return ans

    def find_diff(self, a: int, b: int, c: int, d: int, k: int) -> tuple[list[int], bool]:
        assert b - a == d - c
        length = b - a
        ans = []
        start = 0
        for _ in range(k):
            if self.get(a + start, b) == self.get(c + start, d):
                return ans, False
            lo, hi = start, length
            while hi - lo > 1:
                mid = (lo + hi) >> 1
                if self.get(a + start, a + mid) == self.get(c + start, c + mid):
                    lo = mid
                else:
                    hi = mid
            ans.append(lo)
            start = lo + 1
        return ans, self.get(a + start, b) != self.get(c + start, d)

    def repeat(self, l: int, r: int, w: int) -> int:
        assert 0 <= l < r <= self.sz and w >= 0
        n = r - l
        block = self.get(l, r)
        ans = 0
        cnt = w // n
        base = self._pow(n)
        while cnt:
            if cnt & 1:
                ans = (_mul(ans, base) + block) % _MOD
            block = (_mul(block, base) + block) % _MOD
            base = _mul(base, base)
            cnt >>= 1
        rem = w % n
        return (_mul(ans, self._pow(rem)) + self.get(l, l + rem)) % _MOD

    def repeat_with_one_change(self, l: int, r: int, w: int, i: int, c: str) -> int:
        assert l <= i < r
        old = self.get(i, i + 1)
        delta = ord(c) - old
        if delta < 0:
            delta += _MOD
        n = r - l
        block = (self.get(l, r) + _mul(delta, self._pow(r - i - 1))) % _MOD
        ans = 0
        cnt = w // n
        base = self._pow(n)
        while cnt:
            if cnt & 1:
                ans = (_mul(ans, base) + block) % _MOD
            block = (_mul(block, base) + block) % _MOD
            base = _mul(base, base)
            cnt >>= 1
        rem = w % n
        part = self.get(l, l + rem)
        if i - l < rem:
            part = (part + _mul(delta, self._pow(l + rem - i - 1))) % _MOD
        return (_mul(ans, self._pow(rem)) + part) % _MOD

    def size(self) -> int:
        return self.sz


def getRH(s: str) -> int:
    return RollingHash(s).get_all()
