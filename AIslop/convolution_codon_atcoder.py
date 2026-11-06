"""Convolution modulo 998244353 for AtCoder Codon 0.19.3.

Copy this file as a standalone submission. ``convolution`` is the library API.
"""

MOD = 998244353

def bit_length(x: int) -> int:
    count = 0
    while x:
        count += 1
        x >>= 1
    return count


def _ntt(a, inverse=False, tables=None, scale=0):
    """In-place DIF/DIT NTT; scale optionally normalizes the inverse."""
    n = len(a)
    if not inverse:
        length = n
        while length > 1:
            half = length >> 1
            if length == 2:
                for i in range(0, n, 2):
                    x = a[i]
                    y = a[i + 1]
                    z = x + y
                    if z >= MOD:
                        z -= MOD
                    a[i] = z
                    z = x - y
                    if z < 0:
                        z += MOD
                    a[i + 1] = z
                break
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
            if length == 2 and n > 2:
                for i in range(0, n, 2):
                    x = a[i]
                    y = a[i + 1]
                    z = x + y
                    if z >= MOD:
                        z -= MOD
                    a[i] = z
                    z = x - y
                    if z < 0:
                        z += MOD
                    a[i + 1] = z
                length = 4
                continue
            if tables is None:
                root = pow(3, MOD - 1 - (MOD - 1) // length, MOD)
                roots = [scale if scale and length == n else 1] * half
                for j in range(1, half):
                    roots[j] = roots[j - 1] * root % MOD
            else:
                roots = tables[length]
                if scale and length == n:
                    roots = [w * scale % MOD for w in roots]
            if scale and length == n:
                for j in range(half):
                    x = a[j] * scale % MOD
                    y = a[j + half] * roots[j] % MOD
                    z = x + y
                    if z >= MOD:
                        z -= MOD
                    a[j] = z
                    z = x - y
                    if z < 0:
                        z += MOD
                    a[j + half] = z
                break
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


def _choose_block_ntt(n, m, normal_z):
    """Pick the cheapest overlap-add transform length below the full NTT."""
    z = max(128, 1 << bit_length(n - 1)) << 1
    best_z = 0
    best_cost = 1 << 62
    while z < normal_z and z <= 1 << 23:
        block = z - n + 1
        blocks = (m + block - 1) // block
        cost = (2 * blocks + 1) * z * (bit_length(z) - 1)
        if cost < best_cost:
            best_z, best_cost = z, cost
        z <<= 1
    if 5 * best_cost < 12 * normal_z * (bit_length(normal_z) - 1):
        return best_z
    return 0


def _blocked_convolution(a, b, z):
    """Overlap-add for a short kernel and a much longer input."""
    n, m = len(a), len(b)
    block = z - n + 1
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
        # Only the first n-1 coefficients overlap the preceding block.
        overlap = n - 1 if start else 0
        for i in range(overlap):
            value = out[start + i] + work[i]
            if value >= MOD:
                value -= MOD
            out[start + i] = value
        for i in range(overlap, n + len(part) - 1):
            out[start + i] = work[i]
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
    z = 1 << bit_length(size - 1)
    bz = _choose_block_ntt(n, m, z) if n > 128 and m >= 16384 else 0
    direct_limit = (6 if z <= 512 else 13) * z * (bit_length(z) - 1)
    if n <= 128 or (not bz and n * m <= direct_limit):
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
    if bz:
        return _blocked_convolution(a, b, bz)
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
    iz = pow(z, MOD - 2, MOD)
    _ntt(fa, True, scale=iz)
    return fa[:size]


from C import read(int, Ptr[byte], int) -> int
from C import write(int, Ptr[byte], int) -> int


def read_ints() -> list[int]:
    out = list[int]()
    buf = Ptr[byte](65536)
    number = 0
    in_number = False
    while True:
        got = read(0, buf, 65536)
        if got <= 0:
            break
        for i in range(got):
            c = int(buf[i])
            if c >= 48:
                number = number * 10 + c - 48
                in_number = True
            elif in_number:
                out.append(number)
                number = 0
                in_number = False
    if in_number:
        out.append(number)
    return out


def write_ints(values: list[int]) -> None:
    buf = Ptr[byte](len(values) * 11 + 1)
    p = 0
    for x0 in values:
        x = x0
        start = p
        while x >= 10:
            q = x // 10
            buf[p] = byte(48 + x - q * 10)
            p += 1
            x = q
        buf[p] = byte(48 + x)
        p += 1
        left = start
        right = p - 1
        while left < right:
            t = buf[left]
            buf[left] = buf[right]
            buf[right] = t
            left += 1
            right -= 1
        buf[p] = byte(32)
        p += 1
    if p:
        buf[p - 1] = byte(10)
    else:
        buf[p] = byte(10)
        p += 1
    done = 0
    while done < p:
        w = write(1, buf + done, p - done)
        if w <= 0:
            break
        done += w


if __name__ == "__main__":
    values = read_ints()
    n, m = values[0], values[1]
    a = values[2:2 + n]
    b = values[2 + n:2 + n + m]
    write_ints(convolution(a, b))
