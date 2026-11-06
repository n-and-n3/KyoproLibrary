def ilog_k(x: int, k: int) -> int:
    assert x >= 1 and k >= 2
    ans = 0
    while x >= k:
        x //= k
        ans += 1
    return ans
