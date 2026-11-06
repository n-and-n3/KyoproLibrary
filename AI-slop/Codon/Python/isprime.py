"""Deterministic Miller-Rabin for positive signed 64-bit integers."""


def _mulmod(a: int, b: int, n: int) -> int:
    return int(u128(a) * u128(b) % u128(n))


def _powmod(a: int, e: int, n: int) -> int:
    ans = 1
    while e:
        if e & 1:
            ans = _mulmod(ans, a, n)
        a = _mulmod(a, a, n)
        e >>= 1
    return ans

def is_prime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False

    s = (n - 1).__cttz__()
    d = (n - 1) // (1 << s)

    if n < 4759123141:
      A = [2 ,7 ,61]
    else:
      A = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    for a in A:
        if a % n == 0:
            continue
        x = _powmod(a % n, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = _mulmod(x, x, n)
            if x == n - 1:
                break
        else:
            return False
    return True
