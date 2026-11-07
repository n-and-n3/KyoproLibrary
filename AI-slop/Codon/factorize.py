"""Deterministic primality and factorization for 1 <= n <= 10**18.

Library Checker: primality_test and factorize. No external modules required.
Public API: is_prime(n), factorize(n). factorize returns sorted prime factors.
"""

from math import gcd, sqrt
from random import randrange


class Montgomery:
    """64-bit Montgomery residues for odd moduli at most 10**18."""
    n: u64
    neg_inv: u64
    one: u64
    r2: u64

    def __init__(self, n: int):
        self.n = u64(n)
        x = u64(1)
        for _ in range(6):
            x *= u64(2) - self.n * x
        self.neg_inv = u64(0) - x
        self.one = u64((u128(1) << u128(64)) % u128(self.n))
        self.r2 = u64(u128(self.one) * u128(self.one) % u128(self.n))

    @inline
    def mul(self, a: u64, b: u64) -> u64:
        # The bound n <= 10**18 keeps t + m*n below 2**128.
        t = u128(a) * u128(b)
        m = u64(t) * self.neg_inv
        result = u64((t + u128(m) * u128(self.n)) >> u128(64))
        if result >= self.n:
            result -= self.n
        return result

    def encode(self, a: u64) -> u64:
        return self.mul(a, self.r2)

    def pow(self, a: u64, e: int) -> u64:
        out = self.one
        while e:
            if e & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            e >>= 1
        return out


def _miller_rabin(n: int, extract: bool = False) -> int:
    if n < 2:
        return 1
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return 0
        if n % p == 0:
            return p if extract else 1
    s = (n - 1).__cttz__()
    d = (n - 1) >> s
    ctx = Montgomery(n)
    bases = [2, 7, 61] if n < 4759123141 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    minus_one = ctx.n - ctx.one
    for base in bases:
        a = base
        if a >= n:
            a %= n
        if a == 0:
            continue
        x = ctx.pow(ctx.encode(u64(a)), d)
        if x == ctx.one or x == minus_one:
            continue
        for _ in range(s - 1):
            old = x
            x = ctx.mul(x, x)
            if x == minus_one:
                break
            if x == ctx.one:
                if extract:
                    # R is invertible modulo n, so the gcd of residue
                    # differences equals the gcd of decoded differences.
                    g = gcd(int(old) - int(ctx.one), n)
                    if 1 < g < n:
                        return g
                return 1
        else:
            if extract:
                # Montgomery scaling is invertible modulo n, so this
                # residue difference has the same gcd as the decoded one.
                g = gcd(int(x) - int(ctx.one), n)
                if 1 < g < n:
                    return g
            return 1
    return 0


def is_prime(n: int) -> bool:
    """Exact for 0 <= n <= 10**18."""
    if n > 10**18:
        raise ValueError("n must be <= 10**18")
    return _miller_rabin(n) == 0


def _rho(n: int) -> int:
    """Brent rho with 256-step product batching in Montgomery form."""
    ctx = Montgomery(n)
    mod = ctx.n
    while True:
        y = ctx.encode(u64(randrange(1, n)))
        c = ctx.encode(u64(randrange(1, n)))
        r = 1
        g = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = ctx.mul(y, y) + c
                if y >= mod:
                    y -= mod
            k = 0
            while k < r and g == 1:
                ys = y
                q = ctx.one
                batch = min(256, r - k)
                for _ in range(batch):
                    y = ctx.mul(y, y) + c
                    if y >= mod:
                        y -= mod
                    diff = x - y if x >= y else y - x
                    q = ctx.mul(q, diff)
                g = gcd(int(q), n)
                k += batch
            r <<= 1
        if g == n:
            g = 1
            while g == 1:
                ys = ctx.mul(ys, ys) + c
                if ys >= mod:
                    ys -= mod
                diff = x - ys if x >= ys else ys - x
                g = gcd(int(diff), n)
        if g != n:
            return g


def _fermat_near_square(n: int) -> int:
    a = int(sqrt(float(n)))
    while a * a > n:
        a -= 1
    while (a + 1) * (a + 1) <= n:
        a += 1
    if a * a < n:
        a += 1
    for _ in range(128):
        b2 = a * a - n
        # Squares modulo 16 are 0, 1, 4, or 9.
        if (531 >> (b2 & 15)) & 1:
            b = int(sqrt(float(b2)))
            if b * b == b2:
                f = a - b
                if 1 < f < n:
                    return f
        a += 1
    return 1


def factorize(n: int) -> list[int]:
    """Sorted prime factors with multiplicity; factorize(1) == []."""
    if n < 1 or n > 10**18:
        raise ValueError("factorize requires 1 <= n <= 10**18")
    factors: list[int] = []
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        result = _miller_rabin(m, True)
        if result == 0:
            factors.append(m)
            continue
        if result == 1:
            result = _fermat_near_square(m) if m > 10**12 else 1
            if result == 1:
                result = _rho(m)
        stack.append(result)
        stack.append(m // result)
    factors.sort()
    return factors
