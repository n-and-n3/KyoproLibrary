"""Compact Codon 0.19.3 primality test for 0 <= n <= 10**18.

Base-2 strong Miller-Rabin plus Selfridge strong Lucas (Baillie-PSW).
No counterexample exists below 2**64 in the exhaustive check reported by
Baillie, Fiori, and Wagstaff: https://doi.org/10.1090/mcom/3616
The unrestricted conjecture remains open. No external modules are needed.
"""

from math import sqrt

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

    @inline
    def encode(self, a: u64) -> u64:
        return self.mul(a, self.r2)

    @inline
    def pow(self, a: u64, e: int) -> u64:
        out = self.one
        while e:
            if e & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            e >>= 1
        return out

def _jacobi(a: int, n: int) -> int:
    a %= n
    # Codon -release uses C-style remainder for negative operands.
    if a < 0:
        a += n
    result = 1
    while a:
        while not (a & 1):
            a >>= 1
            if (n & 7) == 3 or (n & 7) == 5:
                result = -result
        a, n = n, a
        if (a & 3) == 3 and (n & 3) == 3:
            result = -result
        a %= n
    return result if n == 1 else 0

def _lucas(n: int, ctx: Montgomery) -> bool:
    root = int(sqrt(float(n)))
    while root * root > n:
        root -= 1
    while (root + 1) * (root + 1) <= n:
        root += 1
    if root * root == n:
        return False
    D = 5
    while True:
        j = _jacobi(D, n)
        if j == -1:
            break
        if j == 0:
            return n == abs(D)
        D = -D - 2 if D > 0 else -D + 2
    Q = (1-D)//4
    q = Q % n
    if q < 0:
        q += n
    dd = D % n
    if dd < 0:
        dd += n
    qm = ctx.encode(u64(q))
    dm = ctx.encode(u64(dd))
    d = n + 1
    s = d.__cttz__()
    d >>= s
    mod = ctx.n
    U = ctx.one
    V = ctx.one
    Qk = qm
    bit = -1
    bits = d
    while bits > 1:
        bits >>= 1
        bit += 1
    while bit >= 0:
        U = ctx.mul(U, V)
        twice = Qk + Qk
        if twice >= mod:
            twice -= mod
        V = ctx.mul(V, V)
        V = V - twice if V >= twice else V + mod - twice
        Qk = ctx.mul(Qk, Qk)
        if (d >> bit) & 1:
            un = U + V
            if un >= mod:
                un -= mod
            du = ctx.mul(dm, U)
            vn = du + V
            if vn >= mod:
                vn -= mod
            if un & u64(1):
                un += mod
            if vn & u64(1):
                vn += mod
            U = un >> u64(1)
            V = vn >> u64(1)
            Qk = ctx.mul(Qk, qm)
        bit -= 1
    if U == u64(0) or V == u64(0):
        return True
    for _ in range(s - 1):
        twice = Qk + Qk
        if twice >= mod:
            twice -= mod
        V = ctx.mul(V, V)
        V = V - twice if V >= twice else V + mod - twice
        Qk = ctx.mul(Qk, Qk)
        if V == u64(0):
            return True
    return False

def is_prime(n: int) -> bool:
    """Return whether n is prime for 0 <= n <= 10**18."""
    if n < 2:
        return False
    if n > 10**18:
        raise ValueError('n must be <= 10**18')
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = d.__cttz__()
    d >>= s
    ctx = Montgomery(n)
    x = ctx.pow(ctx.encode(u64(2)), d)
    if x != ctx.one and x != ctx.n - ctx.one:
        for _ in range(s - 1):
            x = ctx.mul(x, x)
            if x == ctx.n - ctx.one:
                break
        else:
            return False
    return _lucas(n, ctx)
