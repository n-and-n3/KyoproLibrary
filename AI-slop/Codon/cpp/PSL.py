from math import gcd


def fast_isqrt(x: int) -> int:
    if x < 2:
        return x
    a = 1 << ((64 - x.__ctlz__() + 1) >> 1)
    while True:
        b = (a + x // a) >> 1
        if b >= a:
            return a
        a = b


def fast_icbrt(x: int) -> int:
    lo, hi = 0, min(x + 1, 2097152)
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if mid <= x // mid // mid:
            lo = mid
        else:
            hi = mid
    return lo


def ceil_sqrt(x: int) -> int:
    a = fast_isqrt(x)
    return a if a * a == x else a + 1


def exgcd(a: int, b: int) -> tuple[int, int]:
    x0, x1 = 1, 0
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
    return x0, a


def inv(x: int, p: int) -> int:
    a, g = exgcd(x, p)
    assert g == 1
    return (a % p + p) % p


def safe_count_liner(l: int, r: int, c: int, M: int) -> int:
    if l >= r:
        return 0
    return (r - 1 - c) // M - (l - 1 - c) // M


def count_divisors(g: int) -> int:
    ans = 0
    i = 1
    while i * i <= g:
        if g % i == 0:
            ans += 1 if i * i == g else 2
        i += 1
    return ans


def _power_leq(base: int, exponent: int, limit: int) -> int:
    ans = 1
    for _ in range(exponent):
        if ans > limit // base:
            return limit + 1
        ans *= base
    return ans


def _kth_root(x: int, k: int) -> int:
    lo, hi = 1, x + 1
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if _power_leq(mid, k, x) <= x:
            lo = mid
        else:
            hi = mid
    return lo


def calc_f(i: int) -> int:
    ans = 0
    k = 3
    while 1 << k <= i:
        ans += _kth_root(i, k) - 1
        k += 1
    return ans


def ilog_k(x: int, k: int) -> int:
    assert x >= 1 and k >= 2
    ans = 0
    while x >= k:
        x //= k
        ans += 1
    return ans


def cipolla(a: int, p: int) -> int:
    a %= p
    if p == 2 or a == 0:
        return a
    if pow(a, (p - 1) >> 1, p) != 1:
        return -1
    if p & 3 == 3:
        return pow(a, (p + 1) >> 2, p)
    q = p - 1
    s = 0
    while q & 1 == 0:
        q >>= 1
        s += 1
    z = 2
    while pow(z, (p - 1) >> 1, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    x = pow(a, (q + 1) >> 1, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        i = 1
        y = t * t % p
        while y != 1:
            y = y * y % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        x = x * b % p
        t = t * b % p * b % p
        c = b * b % p
        m = i
    return x


def _valuation_interval(l: int, r: int, offset: int, P: int) -> int:
    ans = 0
    power = P
    bound = r - 1 + offset
    while power <= bound:
        ans += bound // power - (l - 1 + offset) // power
        if power > bound // P:
            break
        power *= P
    return ans


def Prod_of_Sum_of_Log(N: int, P: int) -> int:
    # S(i)=i+sum_{m>=2}(floor(i^(1/m))-1). S(i)-i changes only at
    # perfect powers, so valuation sums over each interval use floor counts.
    if N <= 1:
        return 0
    assert P >= 2
    events = []
    k = 2
    while 1 << k <= N:
        b = 2
        while True:
            v = _power_leq(b, k, N)
            if v > N:
                break
            events.append(v)
            b += 1
        k += 1
    events.sort()
    ans = 0
    l = 2
    offset = 0
    i = 0
    while i < len(events):
        x = events[i]
        ans += _valuation_interval(l, x, offset, P)
        while i < len(events) and events[i] == x:
            offset += 1
            i += 1
        l = x
    return ans + _valuation_interval(l, N + 1, offset, P)


def Prod_of_Sum_of_Log_test(N: int, prime: int) -> int:
    ans = 0
    for i in range(2, N + 1):
        s = 1
        for k in range(2, i + 1):
            s += ilog_k(i, k)
        while s % prime == 0:
            s //= prime
            ans += 1
    return ans
