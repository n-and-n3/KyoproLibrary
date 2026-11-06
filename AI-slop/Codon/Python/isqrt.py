def isqrt(n: int) -> int:
    x = int(n ** 0.5)
    while (x + 1) * (x + 1) <= n:
        x += 1
    while x * x > n:
        x -= 1
    return x
