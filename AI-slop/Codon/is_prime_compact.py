"""Compact Codon 0.19.3 primality test for 0 <= n <= 10**18.

FJ32_256 one-witness test below 2**32; base-2 strong Miller-Rabin plus
Selfridge strong Lucas (Baillie-PSW) above it. The FJ32 table is from
https://ceur-ws.org/Vol-1326/020-Forisek.pdf .
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

class Montgomery32:
    """Fast 32-bit residues for odd n < 2**31 (no 64-bit sum overflow)."""
    n: u32
    neg_inv: u32
    one: u32
    r2: u32

    def __init__(self, n: int):
        self.n = u32(n)
        x = u32(1)
        for _ in range(5):
            x *= u32(2) - self.n * x
        self.neg_inv = u32(0) - x
        self.one = u32((u64(1) << u64(32)) % u64(self.n))
        self.r2 = u32((u64(self.one) * u64(self.one)) % u64(self.n))

    @inline
    def mul(self, a: u32, b: u32) -> u32:
        t = u64(a) * u64(b)
        m = u32(t) * self.neg_inv
        result = u32((t + u64(m) * u64(self.n)) >> u64(32))
        if result >= self.n:
            result -= self.n
        return result

    @inline
    def encode(self, a: u64) -> u32:
        return self.mul(u32(a), self.r2)

    @inline
    def pow(self, a: u32, e: int) -> u32:
        out = self.one
        while e:
            if e & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            e >>= 1
        return out


BASE32 = [
    15591, 2018, 166, 7429, 8064, 16045, 10503, 4399, 1949, 1295, 2776, 3620, 560, 3128, 5212, 2657,
    2300, 2021, 4652, 1471, 9336, 4018, 2398, 20462, 10277, 8028, 2213, 6219, 620, 3763, 4852, 5012,
    3185, 1333, 6227, 5298, 1074, 2391, 5113, 7061, 803, 1269, 3875, 422, 751, 580, 4729, 10239,
    746, 2951, 556, 2206, 3778, 481, 1522, 3476, 481, 2487, 3266, 5633, 488, 3373, 6441, 3344,
    17, 15105, 1490, 4154, 2036, 1882, 1813, 467, 3307, 14042, 6371, 658, 1005, 903, 737, 1887,
    7447, 1888, 2848, 1784, 7559, 3400, 951, 13969, 4304, 177, 41, 19875, 3110, 13221, 8726, 571,
    7043, 6943, 1199, 352, 6435, 165, 1169, 3315, 978, 233, 3003, 2562, 2994, 10587, 10030, 2377,
    1902, 5354, 4447, 1555, 263, 27027, 2283, 305, 669, 1912, 601, 6186, 429, 1930, 14873, 1784,
    1661, 524, 3577, 236, 2360, 6146, 2850, 55637, 1753, 4178, 8466, 222, 2579, 2743, 2031, 2226,
    2276, 374, 2132, 813, 23788, 1610, 4422, 5159, 1725, 3597, 3366, 14336, 579, 165, 1375, 10018,
    12616, 9816, 1371, 536, 1867, 10864, 857, 2206, 5788, 434, 8085, 17618, 727, 3639, 1595, 4944,
    2129, 2029, 8195, 8344, 6232, 9183, 8126, 1870, 3296, 7455, 8947, 25017, 541, 19115, 368, 566,
    5674, 411, 522, 1027, 8215, 2050, 6544, 10049, 614, 774, 2333, 3007, 35201, 4706, 1152, 1785,
    1028, 1540, 3743, 493, 4474, 2521, 26845, 8354, 864, 18915, 5465, 2447, 42, 4511, 1660, 166,
    1249, 6259, 2553, 304, 272, 7286, 73, 6554, 899, 2816, 5197, 13330, 7054, 2818, 3199, 811,
    922, 350, 7514, 4452, 3449, 2663, 4708, 418, 1621, 1171, 3471, 88, 11345, 412, 1559, 194,
]

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

def _sprp(ctx, a: int, d: int, s: int) -> bool:
    n = int(ctx.n)
    if a >= n:
        a %= n
    if a == 0:
        return True
    x = ctx.pow(ctx.encode(u64(a)), d)
    if x == ctx.one or x == ctx.n - ctx.one:
        return True
    for _ in range(s-1):
        x = ctx.mul(x, x)
        if x == ctx.n - ctx.one:
            return True
    return False

def is_prime(n: int) -> bool:
    """Return whether n is prime for 0 <= n <= 10**18."""
    if n < 2:
        return False
    if n > 10**18:
        raise ValueError('n must be <= 10**18')
    for p in (2,3,5,7):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = d.__cttz__()
    d >>= s
    if n < 4294967296:
        h = u64(n)
        h = ((h >> u64(16)) ^ h) * u64(0x45d9f3b)
        h = ((h >> u64(16)) ^ h) * u64(0x45d9f3b)
        h = (h >> u64(16)) ^ h
        a = BASE32[int(h & u64(255))]
        if n < 2147483648:
            return _sprp(Montgomery32(n), a, d, s)
        return _sprp(Montgomery(n), a, d, s)
    ctx = Montgomery(n)
    if not _sprp(ctx, 2, d, s):
        return False
    return _lucas(n, ctx)
