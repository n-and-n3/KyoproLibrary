def cipolla(a: int, p: int) -> int:
    # Modular square root for an odd prime p; -1 if no root exists.
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
