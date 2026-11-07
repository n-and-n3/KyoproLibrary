"""Deterministic primality and factorization for 0 <= n < 2**64.

Library Checker: primality_test and factorize (both restrict n to 10**18).
Public API: is_prime(n), factorize(n). factorize returns sorted prime factors.
"""

from math import gcd, isqrt
from random import randrange


_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
_BASES64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def _miller_rabin(n, extract=False):
    """Return 0 for prime, 1 for composite, or a factor when extract=True."""
    if n < 2:
        return 1
    for p in _SMALL:
        if n == p:
            return 0
        if n % p == 0:
            return p if extract else 1
    s = ((n - 1) & (1 - n)).bit_length() - 1
    d = (n - 1) >> s
    bases = (2, 7, 61) if n < 4759123141 else _BASES64
    for base in bases:
        a = base % n
        if not a:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            old = x
            x = x * x % n
            if x == n - 1:
                break
            if x == 1:
                if extract:
                    g = gcd(old - 1, n)
                    if 1 < g < n:
                        return g
                return 1
        else:
            return 1
    return 0


def is_prime(n):
    """Exact for integers below 2**64."""
    if n >= 1 << 64:
        raise ValueError("n must be less than 2**64")
    return _miller_rabin(n) == 0


def _rho(n):
    """Brent's batched-GCD Pollard rho; n must be odd and composite."""
    while True:
        y = randrange(1, n)
        c = randrange(1, n)
        r = 1
        g = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (pow(y, 2, n) + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                q = 1
                batch = min(128, r - k)
                for _ in range(batch):
                    y = (pow(y, 2, n) + c) % n
                    q = q * (x - y) % n
                g = gcd(q, n)
                k += batch
            r <<= 1
        if g == n:
            g = 1
            while g == 1:
                ys = (pow(ys, 2, n) + c) % n
                g = gcd(x - ys, n)
        if g != n:
            return g


def _fermat_near_square(n):
    """Catch close semiprimes, including the special cases in Library Checker."""
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(128):
        b2 = a * a - n
        # Squares modulo 16 are 0, 1, 4, or 9.
        if (531 >> (b2 & 15)) & 1:
            b = isqrt(b2)
            if b * b == b2:
                f = a - b
                if 1 < f < n:
                    return f
        a += 1
    return 1


def factorize(n):
    """Sorted prime factors with multiplicity; factorize(1) == []."""
    if not 1 <= n < 1 << 64:
        raise ValueError("factorize requires 1 <= n < 2**64")
    factors = []
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
