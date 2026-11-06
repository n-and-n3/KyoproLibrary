from math import gcd


def _isqrt(n: int) -> int:
    if n < 2:
        return n
    x = 1 << ((64 - n.__ctlz__() + 1) >> 1)
    while True:
        y = (x + n // x) >> 1
        if y >= x:
            return x
        x = y


def fast_isqrt(x: int) -> int:
    return _isqrt(x)


def fast_icbrt(x: int) -> int:
    lo, hi = 0, min(x + 1, 2097152)
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if mid <= x // mid // mid:
            lo = mid
        else:
            hi = mid
    return lo


def safe_pow(a: int, b: int) -> int:
    limit = 2000000000000000000
    ans = 1
    while b:
        if b & 1:
            if ans > limit // a:
                return limit
            ans *= a
        b >>= 1
        if b:
            if a > limit // a:
                a = limit
            else:
                a *= a
    return ans


def _quotient_product_mod(factors: list[int], den: int, mod: int) -> int:
    for i in range(len(factors)):
        g = gcd(factors[i], den)
        factors[i] //= g
        den //= g
    assert den == 1
    ans = 1
    for x in factors:
        ans = ans * (x % mod) % mod
    return ans


def sum_iisqrti(N: int, MOD: int = 998244353) -> int:
    if N <= 0:
        return 0
    M = _isqrt(N)
    m = M - 1
    s2 = _quotient_product_mod([m, m + 1, 2 * m + 1], 6, MOD)
    s3 = _quotient_product_mod([m, m + 1], 2, MOD)
    s3 = s3 * s3 % MOD
    s4 = _quotient_product_mod([m, m + 1, 2 * m + 1, 3 * m * m + 3 * m - 1], 30, MOD)
    full = (2 * s4 + 3 * s3 + s2) % MOD
    tail = _quotient_product_mod([N - M * M + 1, N + M * M], 2, MOD)
    return (full + M * tail) % MOD


def kth_root_integer(x: int, k: int) -> int:
    if k <= 1:
        return x if k else 1
    if x <= 1:
        return x
    lo, hi = 1, min(x + 1, 1 << ((64 - x.__ctlz__() + k - 1) // k + 1))
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if safe_pow(mid, k) <= x:
            lo = mid
        else:
            hi = mid
    return lo


def Sum_of_Prod_of_Root(N: int, MOD: int) -> int:
    if N <= 0:
        return 0
    assert MOD >= 2
    bound = fast_icbrt(N)
    modinv = [0] * (bound + 1)
    ppower = [0] * (bound + 1)
    residue = [0] * (bound + 1)
    if bound >= 1:
        modinv[1] = 1
        residue[1] = 1
    for i in range(2, bound + 1):
        if i < MOD:
            residue[i] = i
            modinv[i] = (MOD - modinv[MOD % i] * (MOD // i) % MOD) % MOD
        elif i % MOD == 0:
            j = i
            while j % MOD == 0:
                j //= MOD
                ppower[i] += 1
            residue[i] = j % MOD
            modinv[i] = modinv[j]
        else:
            residue[i] = i % MOD
            modinv[i] = modinv[i % MOD]
    transitions = [(N + 1, 1)]
    bits = 0
    x = N
    while x:
        bits += 1
        x >>= 1
    for k in range(3, bits + 1):
        j = 2
        while True:
            power = safe_pow(j, k)
            if power > N:
                break
            transitions.append((power, j))
            j += 1
    transitions.sort()
    product = 1
    prev = 0
    ans = 0
    zero_pow = 0
    for threshold, j in transitions:
        current = sum_iisqrti(threshold - 1, MOD)
        if zero_pow == 0:
            ans = (ans + product * ((current - prev + MOD) % MOD)) % MOD
        zero_pow += ppower[j] - ppower[j - 1]
        product = product * modinv[j - 1] % MOD * residue[j] % MOD
        prev = current
    return ans


def Sum_of_Prod_of_Root_test(N: int, MOD: int) -> int:
    ans = 0
    for i in range(1, N + 1):
        term = 1
        for k in range(1, 61):
            term = term * kth_root_integer(i, k) % MOD
        ans = (ans + term) % MOD
    return ans
