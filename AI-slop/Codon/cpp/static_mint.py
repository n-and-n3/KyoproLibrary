class static_modint:
    _val: int
    MOD: int

    def __init__(self, x: int = 0, MOD: int = 998244353):
        self.MOD = MOD
        self._val = x % MOD
        if self._val < 0:
            self._val += MOD

    def val(self) -> int:
        return self._val

    def __int__(self) -> int:
        return self._val

    def __add__(self, other: static_modint) -> static_modint:
        assert self.MOD == other.MOD
        x = self._val + other._val
        if x >= self.MOD:
            x -= self.MOD
        return static_modint(x, self.MOD)

    def __sub__(self, other: static_modint) -> static_modint:
        assert self.MOD == other.MOD
        x = self._val - other._val
        if x < 0:
            x += self.MOD
        return static_modint(x, self.MOD)

    def __mul__(self, other: static_modint) -> static_modint:
        assert self.MOD == other.MOD
        return static_modint(self._val * other._val % self.MOD, self.MOD)

    def inv(self) -> static_modint:
        a, b = self._val, self.MOD
        x0, x1 = 1, 0
        while b:
            q = a // b
            a, b = b, a - q * b
            x0, x1 = x1, x0 - q * x1
        if a != 1:
            raise ZeroDivisionError('modular inverse does not exist')
        return static_modint(x0, self.MOD)

    def __truediv__(self, other: static_modint) -> static_modint:
        return self * other.inv()

    def pow(self, n: int) -> static_modint:
        if n < 0:
            return self.inv().pow(-n)
        x = self
        ans = static_modint(1, self.MOD)
        while n:
            if n & 1:
                ans = ans * x
            x = x * x
            n >>= 1
        return ans

    def __pow__(self, n: int) -> static_modint:
        return self.pow(n)

    def __eq__(self, other: static_modint) -> bool:
        return self.MOD == other.MOD and self._val == other._val

    def __lt__(self, other: static_modint) -> bool:
        return self._val < other._val

    def __gt__(self, other: static_modint) -> bool:
        return self._val > other._val
