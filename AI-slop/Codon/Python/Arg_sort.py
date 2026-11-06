"""Codon port of Python/Arg_sort.py."""

def area(p):
    x, y = p[0], p[1]
    if y < 0:
        return 3
    elif x < 0:
        return 2
    else:
        return 1


def arg_cmp(p, q):
    ap = area(p)
    aq = area(q)
    if ap < aq:
        return -1
    elif ap > aq:
        return 1
    else:
        px, py = p[0], p[1]
        qx, qy = q[0], q[1]
        z = px * qy - py * qx
        if z > 0:
            return -1
        elif z < 0:
            return 1
        else:
            return 0


def sample(array):
    """Sort by polar angle in place, preserving the original API."""
    n = len(array)
    work = array[:]
    width = 1
    while width < n:
        for left in range(0, n, width << 1):
            mid = min(left + width, n)
            right = min(left + (width << 1), n)
            i, j, k = left, mid, left
            while i < mid and j < right:
                if arg_cmp(array[i], array[j]) <= 0:
                    work[k] = array[i]
                    i += 1
                else:
                    work[k] = array[j]
                    j += 1
                k += 1
            while i < mid:
                work[k] = array[i]
                i += 1
                k += 1
            while j < right:
                work[k] = array[j]
                j += 1
                k += 1
        for k in range(n):
            array[k] = work[k]
        width <<= 1
