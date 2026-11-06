def isqrt(n: int) -> int:
    assert n >= 0
    if n < 2:
        return n
    x = 1 << ((64 - n.__ctlz__() + 1) >> 1)
    while True:
        y = (x + n // x) >> 1
        if y >= x:
            return x
        x = y
