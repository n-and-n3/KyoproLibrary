"""Convolution modulo 998244353 for PyPy 3 (yosupo/convolution_mod).

Copy this file as a standalone submission.  ``convolution`` is the library API.
"""

MOD = 998244353


def _ntt(a, inverse=False, tables=None):
    """In-place, unnormalised NTT. Forward: DIF; inverse: DIT."""
    n = len(a)
    if not inverse:
        length = n
        while length > 1:
            half = length >> 1
            if tables is None:
                root = pow(3, (MOD - 1) // length, MOD)
                roots = [1] * half
                for j in range(1, half):
                    roots[j] = roots[j - 1] * root % MOD
            else:
                roots = tables[length]
            for i in range(0, n, length):
                for j in range(half):
                    x = a[i + j]
                    y = a[i + j + half]
                    z = x + y
                    if z >= MOD:
                        z -= MOD
                    a[i + j] = z
                    z = x - y
                    if z < 0:
                        z += MOD
                    a[i + j + half] = z * roots[j] % MOD
            length >>= 1
    else:
        length = 2
        while length <= n:
            half = length >> 1
            if tables is None:
                root = pow(3, MOD - 1 - (MOD - 1) // length, MOD)
                roots = [1] * half
                for j in range(1, half):
                    roots[j] = roots[j - 1] * root % MOD
            else:
                roots = tables[length]
            for i in range(0, n, length):
                for j in range(half):
                    x = a[i + j]
                    y = a[i + j + half] * roots[j] % MOD
                    z = x + y
                    if z >= MOD:
                        z -= MOD
                    a[i + j] = z
                    z = x - y
                    if z < 0:
                        z += MOD
                    a[i + j + half] = z
            length <<= 1


def _tables(z):
    forward = {}
    inverse = {}
    length = 2
    while length <= z:
        root = pow(3, (MOD - 1) // length, MOD)
        iroot = pow(root, MOD - 2, MOD)
        rf = [1] * (length >> 1)
        ri = [1] * (length >> 1)
        for j in range(1, length >> 1):
            rf[j] = rf[j - 1] * root % MOD
            ri[j] = ri[j - 1] * iroot % MOD
        forward[length] = rf
        inverse[length] = ri
        length <<= 1
    return forward, inverse


def _blocked_convolution(a, b):
    """Overlap-add for a short kernel and a much longer input."""
    n, m = len(a), len(b)
    block = max(128, 1 << (n - 1).bit_length())
    z = block << 1
    if z > 1 << 23:
        raise ValueError("NTT length exceeds 2^23")
    forward, inverse = _tables(z)
    kernel = a[:] + [0] * (z - n)
    _ntt(kernel, tables=forward)
    invz = pow(z, MOD - 2, MOD)
    for i in range(z):
        kernel[i] = kernel[i] * invz % MOD
    out = [0] * (n + m - 1)
    for start in range(0, m, block):
        part = b[start:start + block]
        work = part + [0] * (z - len(part))
        _ntt(work, tables=forward)
        for i in range(z):
            work[i] = work[i] * kernel[i] % MOD
        _ntt(work, True, inverse)
        for i in range(n + len(part) - 1):
            value = out[start + i] + work[i]
            if value >= MOD:
                value -= MOD
            out[start + i] = value
    return out


def _constant_convolution(value, width, other):
    """Convolve a constant vector using a sliding window sum."""
    m = len(other)
    out = [0] * (width + m - 1)
    total = 0
    for k in range(len(out)):
        if k < m:
            total += other[k]
        if k >= width:
            total -= other[k - width]
        if total >= MOD:
            total -= MOD
        elif total < 0:
            total += MOD
        out[k] = total if value == 1 else total * value % MOD
    return out


def convolution(a, b):
    """Return polynomial product mod 998244353; accepts coefficient lists."""
    n, m = len(a), len(b)
    if not n or not m:
        return []
    size = n + m - 1
    al = 0
    while al < n and not a[al]:
        al += 1
    if al == n:
        return [0] * size
    ar = n
    while not a[ar - 1]:
        ar -= 1
    bl = 0
    while bl < m and not b[bl]:
        bl += 1
    if bl == m:
        return [0] * size
    br = m
    while not b[br - 1]:
        br -= 1
    if al or bl or ar != n or br != m:
        shift = al + bl
        c = convolution(a[al:ar], b[bl:br])
        return [0] * shift + c + [0] * (size - shift - len(c))
    if n == 1:
        x = a[0]
        return [x * y % MOD for y in b]
    if m == 1:
        x = b[0]
        return [x * y % MOD for y in a]
    if n >= 64 and all(a[i] == a[0] for i in range(1, n)):
        return _constant_convolution(a[0], n, b)
    if m >= 64 and all(b[i] == b[0] for i in range(1, m)):
        return _constant_convolution(b[0], m, a)
    if n > m:
        a, b = b, a
        n, m = m, n
    z = 1 << (size - 1).bit_length()
    if n >= 33 and m >= 16384:
        block = max(128, 1 << (n - 1).bit_length())
        bz = block << 1
        blocks = (m + block - 1) // block
        if 5 * (2 * blocks + 1) * bz * (bz.bit_length() - 1) < 12 * z * (z.bit_length() - 1):
            return _blocked_convolution(a, b)
    if (min(n, m) <= 100 and n * m <= 100000) or n * m <= 4096:
        if n < m:
            a, b = b, a
            n, m = m, n
        c = [0] * size
        for j in range(m):
            bj = b[j]
            if bj:
                for i in range(n):
                    c[i + j] = (c[i + j] + a[i] * bj) % MOD
        return c
    if z > 1 << 23:
        raise ValueError("NTT length exceeds 2^23")
    fa = a[:] + [0] * (z - n)
    _ntt(fa)
    if a == b:
        for i in range(z):
            fa[i] = fa[i] * fa[i] % MOD
    else:
        fb = b[:] + [0] * (z - m)
        _ntt(fb)
        for i in range(z):
            fa[i] = fa[i] * fb[i] % MOD
    _ntt(fa, True)
    iz = pow(z, MOD - 2, MOD)
    return [fa[i] * iz % MOD for i in range(size)]


def _read_ints(data):
    number = 0
    in_number = False
    for c in data:
        if c >= 48:
            number = number * 10 + c - 48
            in_number = True
        elif in_number:
            yield number
            number = 0
            in_number = False
    if in_number:
        yield number


if __name__ == "__main__":
    import sys

    values = _read_ints(sys.stdin.buffer.read())
    n = next(values)
    m = next(values)
    a = [next(values) for _ in range(n)]
    b = [next(values) for _ in range(m)]
    sys.stdout.write(" ".join(map(str, convolution(a, b))) + "\n")
