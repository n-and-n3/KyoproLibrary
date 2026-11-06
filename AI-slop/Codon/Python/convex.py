"""Codon port of Python/convex.py."""

def convex(array):
    N = len(array)
    if N == 0:
        return []

    mx,my,mi = array[0][0], array[0][1], 0
    for i,t in enumerate(array):
        x,y = t
        if x < mx or (x == mx and y <= my):
            mx = x
            my = y
            mi = i

    P = [(t[0]-mx,t[1]-my,i) for i,t in enumerate(array) if i != mi]

    def comarg(a,b): # a > b -> +1, a == b -> 0, a < b -> -1
        outer = a[0]*b[1] - a[1]*b[0]
        if outer > 0:
            return -1
        elif outer < 0:
            return +1
        else:
            la = a[0]**2+a[1]**2
            lb = b[0]**2+b[1]**2
            if la < lb:
                return -1
            elif la > lb:
                return +1
            else:
                return 0

    work = P[:]
    width = 1
    while width < len(P):
        for left in range(0, len(P), width << 1):
            mid = min(left + width, len(P))
            right = min(left + (width << 1), len(P))
            i, j, k = left, mid, left
            while i < mid and j < right:
                if comarg(P[i], P[j]) <= 0:
                    work[k] = P[i]
                    i += 1
                else:
                    work[k] = P[j]
                    j += 1
                k += 1
            while i < mid:
                work[k] = P[i]
                i += 1
                k += 1
            while j < right:
                work[k] = P[j]
                j += 1
                k += 1
        for k in range(len(P)):
            P[k] = work[k]
        width <<= 1

    stack = [(0,0,mi)]
    for t in P:
        if t[0] == 0 and t[1] == 0:
            continue
        while len(stack) >= 2:
            a, b = stack[-2], stack[-1]
            outer = (b[0]-a[0])*(t[1]-b[1]) - (b[1]-a[1])*(t[0]-b[0])
            if outer > 0:
                break
            stack.pop()
        stack.append(t)

    return stack
