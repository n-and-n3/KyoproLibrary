"""Codon port of Python/QuotientRange.py."""

def _isqrt(n: int) -> int:
    if n < 0:
        raise ValueError("square root of a negative number")
    if n < 2:
        return n
    x = 1 << ((65 - n.__ctlz__()) >> 1)
    while True:
        y = (x + n // x) >> 1
        if y >= x:
            return x
        x = y


def quotient_range(N):
    ans = [] # (l,r,v) := x in [l,r) の区間において、N//x = z である。
    sqrtN = _isqrt(N)
    m = N
    for i in range(1,sqrtN+1):
        ans.append((i,i+1,N//i))
        m = N//i
    for i in range(m-1,0,-1):
        L = N//(i+1)+1
        R = N//i+1
        if L < R:
          ans.append((L,R,i))
    return ans


def quotient_range_generator(N):
    sqrtN = _isqrt(N)
    m = N
    for i in range(1,sqrtN+1):
        yield (i,i+1,N//i)
        m = N//i
    for i in range(m-1,0,-1):
        L = N//(i+1)+1
        R = N//i+1
        if L < R:
          yield (L,R,i)
