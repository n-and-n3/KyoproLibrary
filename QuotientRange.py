# 要検証問題

import math

def quotient_range(N):
    ans = [] # (l,r,v) := x in [l,r) の区間において、N//x = z である。
    sqrtN = math.isqrt(N)
    for i in range(1,sqrtN+1):
        ans.append((i,i+1,N//i))
    for i in range(sqrtN - (N==sqrtN**2),0,-1):
        L = N//(i+1)+1
        R = N//i+1
        ans.append((L,R,i))
    return ans

def quotient_range_yield(N):
    ans = [] # (l,r,v) := x in [l,r) の区間において、N//x = z である。
    sqrtN = math.isqrt(N)
    for i in range(1,sqrtN+1):
        yield (i,i+1,N//i)
    for i in range(sqrtN - (N==sqrtN**2),0,-1):
        L = N//(i+1)+1
        R = N//i+1
        yield (L,R,i)
    return ans

def main():
    N = 9
    print(quotient_range(N))
    print(*[N//i for i in range(1,N+1)])
    print()
    N = 15
    print(quotient_range(N))
    print(*[N//i for i in range(1,N+1)])
    print()

main()