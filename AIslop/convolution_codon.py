"""Standalone convolution modulo 998244353 for Codon.

The public API is ``convolution(a, b)``. Inputs use yosupo's nonnegative
coefficient range. The NTT uses Montgomery residues and SIMD radix-4
butterflies where eight lanes are available.
"""

MOD = 998244353
MONT_ONE = 301989884
MONT_R2 = 932051910
MONT_NINV = 998244351


def mm(a: int, b: int) -> int:
    t = a * b
    q = ((t & 0xffffffff) * MONT_NINV) & 0xffffffff
    r = (t + q * MOD) >> 32
    if r >= MOD:
        r -= MOD
    return r


from simd import Vec


def mmv(a: Vec[u32, 8], b: Vec[u32, 8]) -> Vec[u32, 8]:
    aa = a.cast(u64)
    bb = b.cast(u64)
    t = aa * bb
    mask = Vec[u64, 8](u64(0xffffffff))
    modulus = Vec[u64, 8](u64(998244353))
    ninv = Vec[u64, 8](u64(998244351))
    q = ((t & mask) * ninv) & mask
    r = ((t + q * modulus) >> 32).cast(u32)
    return r.min(r - Vec[u32, 8](u32(MOD)))


def addv(a: Vec[u32, 8], b: Vec[u32, 8]) -> Vec[u32, 8]:
    c = a + b
    return c.min(c - Vec[u32, 8](u32(MOD)))


def subv(a: Vec[u32, 8], b: Vec[u32, 8]) -> Vec[u32, 8]:
    c = a + Vec[u32, 8](u32(MOD)) - b
    return c.min(c - Vec[u32, 8](u32(MOD)))


def pointwise(a: list[u32], b: list[u32]) -> None:
    pa = a._ptr
    pb = b._ptr
    for i in range(0, len(a), 8):
        mmv(Vec[u32, 8](pa + i), Vec[u32, 8](pb + i)).store(pa + i)


def pointwise_square(a: list[u32]) -> None:
    pa = a._ptr
    for i in range(0, len(a), 8):
        v = Vec[u32, 8](pa + i)
        mmv(v, v).store(pa + i)


def normalize(a: list[u32], iz: int) -> None:
    pa = a._ptr
    iv = Vec[u32, 8](u32(iz))
    for i in range(0, len(a), 8):
        mmv(Vec[u32, 8](pa + i), iv).store(pa + i)


def ntt_plan(n: int):
    logn = (n - 1).bit_length()
    normal_roots = [pow(3, (MOD - 1) >> k, MOD) for k in range(logn + 1)]
    roots = [mm(x, MONT_R2) for x in normal_roots]
    iroots = [mm(pow(x, MOD - 2, MOD), MONT_R2) for x in normal_roots]
    rate2 = [0] * logn
    rate3 = [0] * logn
    irate2 = [0] * logn
    irate3 = [0] * logn
    x2 = y2 = x3 = y3 = MONT_ONE
    for k in range(logn - 1):
        rate2[k] = mm(roots[k + 2], x2)
        irate2[k] = mm(iroots[k + 2], y2)
        x2 = mm(x2, iroots[k + 2])
        y2 = mm(y2, roots[k + 2])
    for k in range(logn - 2):
        rate3[k] = mm(roots[k + 3], x3)
        irate3[k] = mm(iroots[k + 3], y3)
        x3 = mm(x3, iroots[k + 3])
        y3 = mm(y3, roots[k + 3])
    return roots, iroots, rate2, rate3, irate2, irate3


def ntt(a: list[u32], inverse: bool, plan, filled: int) -> None:
    n = len(a)
    buf = a._ptr
    logn = (n - 1).bit_length()
    roots, iroots, rate2, rate3, irate2, irate3 = plan
    if not inverse:
        h = 0
        # The first radix-4 stage has no rotation between blocks.
        if logn >= 5 and (logn & 1) and filled <= n >> 1:
            p = n >> 2
            if filled <= p:
                for j in range(p):
                    v = buf[j]
                    buf[j + p] = v
                    buf[j + 2 * p] = v
                    buf[j + 3 * p] = v
            else:
                imagv = Vec[u32, 8](u32(roots[2]))
                for j in range(0, p, 8):
                    v0 = Vec[u32, 8](buf + j)
                    v1 = Vec[u32, 8](buf + j + p)
                    w = mmv(v1, imagv)
                    addv(v0, v1).store(buf + j)
                    subv(v0, v1).store(buf + j + p)
                    addv(v0, w).store(buf + j + 2 * p)
                    subv(v0, w).store(buf + j + 3 * p)
            h = 2
        while h < logn:
            if logn - h == 1:
                p = 1 << (logn - h - 1)
                rot = MONT_ONE
                for s in range(1 << h):
                    off = s << (logn - h)
                    for j in range(p):
                        x = int(buf[off + j])
                        y = mm(int(buf[off + j + p]), rot)
                        z = x + y
                        if z >= MOD: z -= MOD
                        buf[off + j] = u32(z)
                        z = x - y
                        if z < 0: z += MOD
                        buf[off + j + p] = u32(z)
                    if s + 1 < (1 << h):
                        c = ((s + 1) & -(s + 1)).bit_length() - 1
                        rot = mm(rot, rate2[c])
                h += 1
            else:
                p = 1 << (logn - h - 2)
                rot = MONT_ONE
                imag = roots[2]
                for s in range(1 << h):
                    off = s << (logn - h)
                    r2 = mm(rot, rot)
                    r3 = mm(r2, rot)
                    jstart = 0
                    if p >= 8:
                        rv = Vec[u32, 8](u32(rot))
                        r2v = Vec[u32, 8](u32(r2))
                        r3v = Vec[u32, 8](u32(r3))
                        iv = Vec[u32, 8](u32(imag))
                        for j in range(0, p, 8):
                            v0 = Vec[u32, 8](buf + off + j)
                            v1 = mmv(Vec[u32, 8](buf + off + j + p), rv)
                            v2 = mmv(Vec[u32, 8](buf + off + j + 2 * p), r2v)
                            v3 = mmv(Vec[u32, 8](buf + off + j + 3 * p), r3v)
                            t0 = addv(v0, v2)
                            t1 = addv(v1, v3)
                            t2 = subv(v0, v2)
                            t3 = mmv(subv(v1, v3), iv)
                            addv(t0, t1).store(buf + off + j)
                            subv(t0, t1).store(buf + off + j + p)
                            addv(t2, t3).store(buf + off + j + 2 * p)
                            subv(t2, t3).store(buf + off + j + 3 * p)
                        jstart = p
                    for j in range(jstart, p):
                        v0 = int(buf[off + j])
                        v1 = mm(int(buf[off + j + p]), rot)
                        v2 = mm(int(buf[off + j + 2 * p]), r2)
                        v3 = mm(int(buf[off + j + 3 * p]), r3)
                        t0 = v0 + v2
                        if t0 >= MOD: t0 -= MOD
                        t1 = v1 + v3
                        if t1 >= MOD: t1 -= MOD
                        t2 = v0 - v2
                        if t2 < 0: t2 += MOD
                        diff = v1 - v3
                        if diff < 0: diff += MOD
                        t3 = mm(diff, imag)
                        z = t0 + t1
                        if z >= MOD: z -= MOD
                        buf[off + j] = u32(z)
                        z = t0 - t1
                        if z < 0: z += MOD
                        buf[off + j + p] = u32(z)
                        z = t2 + t3
                        if z >= MOD: z -= MOD
                        buf[off + j + 2 * p] = u32(z)
                        z = t2 - t3
                        if z < 0: z += MOD
                        buf[off + j + 3 * p] = u32(z)
                    if s + 1 < (1 << h):
                        c = ((s + 1) & -(s + 1)).bit_length() - 1
                        rot = mm(rot, rate3[c])
                h += 2
    else:
        h = logn
        while h:
            if h == 1:
                h -= 1
                p = 1 << (logn - h - 1)
                rot = MONT_ONE
                for s in range(1 << h):
                    off = s << (logn - h)
                    for j in range(p):
                        x = int(buf[off + j])
                        y = int(buf[off + j + p])
                        z = x + y
                        if z >= MOD: z -= MOD
                        buf[off + j] = u32(z)
                        z = x - y
                        if z < 0: z += MOD
                        buf[off + j + p] = u32(mm(z, rot))
                    if s + 1 < (1 << h):
                        c = ((s + 1) & -(s + 1)).bit_length() - 1
                        rot = mm(rot, irate2[c])
            else:
                h -= 2
                p = 1 << (logn - h - 2)
                rot = MONT_ONE
                iimag = iroots[2]
                for s in range(1 << h):
                    off = s << (logn - h)
                    r2 = mm(rot, rot)
                    r3 = mm(r2, rot)
                    jstart = 0
                    if p >= 8:
                        rv = Vec[u32, 8](u32(rot))
                        r2v = Vec[u32, 8](u32(r2))
                        r3v = Vec[u32, 8](u32(r3))
                        iv = Vec[u32, 8](u32(iimag))
                        for j in range(0, p, 8):
                            v0 = Vec[u32, 8](buf + off + j)
                            v1 = Vec[u32, 8](buf + off + j + p)
                            v2 = Vec[u32, 8](buf + off + j + 2 * p)
                            v3 = Vec[u32, 8](buf + off + j + 3 * p)
                            t0 = addv(v0, v1)
                            t1 = subv(v0, v1)
                            t2 = addv(v2, v3)
                            t3 = mmv(subv(v2, v3), iv)
                            addv(t0, t2).store(buf + off + j)
                            mmv(addv(t1, t3), rv).store(buf + off + j + p)
                            mmv(subv(t0, t2), r2v).store(buf + off + j + 2 * p)
                            mmv(subv(t1, t3), r3v).store(buf + off + j + 3 * p)
                        jstart = p
                    for j in range(jstart, p):
                        v0 = int(buf[off + j])
                        v1 = int(buf[off + j + p])
                        v2 = int(buf[off + j + 2 * p])
                        v3 = int(buf[off + j + 3 * p])
                        t0 = v0 + v1
                        if t0 >= MOD: t0 -= MOD
                        t1 = v0 - v1
                        if t1 < 0: t1 += MOD
                        t2 = v2 + v3
                        if t2 >= MOD: t2 -= MOD
                        diff = v2 - v3
                        if diff < 0: diff += MOD
                        t3 = mm(diff, iimag)
                        z = t0 + t2
                        if z >= MOD: z -= MOD
                        buf[off + j] = u32(z)
                        z = t1 + t3
                        if z >= MOD: z -= MOD
                        buf[off + j + p] = u32(mm(z, rot))
                        z = t0 - t2
                        if z < 0: z += MOD
                        buf[off + j + 2 * p] = u32(mm(z, r2))
                        z = t1 - t3
                        if z < 0: z += MOD
                        buf[off + j + 3 * p] = u32(mm(z, r3))
                    if s + 1 < (1 << h):
                        c = ((s + 1) & -(s + 1)).bit_length() - 1
                        rot = mm(rot, irate3[c])


def mont_array(a: list[int], z: int) -> list[u32]:
    out = [u32(0)] * z
    src = a._ptr
    dst = out._ptr
    r2 = Vec[u32, 8](u32(MONT_R2))
    end = len(a) & ~7
    for i in range(0, end, 8):
        mmv(Vec[i64, 8](src + i).cast(u32), r2).store(dst + i)
    for i in range(end, len(a)):
        dst[i] = u32(mm(a[i], MONT_R2))
    return out


def finish(a: list[u32], size: int, iz: int) -> list[int]:
    out = [0] * size
    src = a._ptr
    dst = out._ptr
    iv = Vec[u32, 8](u32(iz))
    end = size & ~7
    for i in range(0, end, 8):
        mmv(Vec[u32, 8](src + i), iv).cast(i64).store(dst + i)
    for i in range(end, size):
        out[i] = mm(int(src[i]), iz)
    return out


def choose_block_ntt(n: int, m: int, normal_z: int) -> int:
    """Pick the cheapest overlap-add transform length below the full NTT."""
    z = max(128, 1 << (n - 1).bit_length()) << 1
    best_z = 0
    best_cost = 1 << 62
    while z < normal_z and z <= 1 << 23:
        block = z - n + 1
        blocks = (m + block - 1) // block
        cost = (2 * blocks + 1) * z * (z.bit_length() - 1)
        if cost < best_cost:
            best_z, best_cost = z, cost
        z <<= 1
    if 5 * best_cost < 12 * normal_z * (normal_z.bit_length() - 1):
        return best_z
    return 0


def blocked_convolution(a: list[int], b: list[int], z: int) -> list[int]:
    """Overlap-add; reuse the short input transform across all blocks."""
    n, m = len(a), len(b)
    block = z - n + 1
    if z > 1 << 23:
        raise ValueError("NTT length exceeds 2^23")
    kernel = mont_array(a, z)
    plan = ntt_plan(z)
    ntt(kernel, False, plan, n)
    iz = pow(z, MOD - 2, MOD)
    # Keep the scaled kernel in ordinary residues. Multiplying it by a
    # Montgomery-transformed block produces ordinary residues for the INTT.
    normalize(kernel, iz)
    out = [0] * (n + m - 1)
    for start in range(0, m, block):
        part = b[start:start + block]
        work = mont_array(part, z)
        ntt(work, False, plan, len(part))
        pointwise(work, kernel)
        ntt(work, True, plan, 0)
        # Only the first n-1 coefficients overlap the preceding block.
        overlap = n - 1 if start else 0
        for i in range(overlap):
            v = out[start + i] + int(work[i])
            if v >= MOD:
                v -= MOD
            out[start + i] = v
        for i in range(overlap, n + len(part) - 1):
            out[start + i] = int(work[i])
    return out


def constant_convolution(value: int, width: int, other: list[int]) -> list[int]:
    """Convolve a constant vector using a sliding window sum."""
    m = len(other)
    out = [0] * (width + m - 1)
    uniform = True
    for i in range(1, m):
        if other[i] != other[0]:
            uniform = False
            break
    if uniform:
        step = value * other[0] % MOD
        total = 0
        for k in range(len(out)):
            if k < m:
                total += step
            if k >= width:
                total -= step
            if total >= MOD:
                total -= MOD
            elif total < 0:
                total += MOD
            out[k] = total
        return out
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


def convolution(a: list[int], b: list[int]) -> list[int]:
    """Return polynomial product modulo 998244353."""
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
    if n >= 64:
        constant = True
        for i in range(1, n):
            if a[i] != a[0]:
                constant = False
                break
        if constant:
            return constant_convolution(a[0], n, b)
    if m >= 64:
        constant = True
        for i in range(1, m):
            if b[i] != b[0]:
                constant = False
                break
        if constant:
            return constant_convolution(b[0], m, a)
    if min(n, m) <= 12 or (min(n, m) <= 32 and n * m <= 400000) or n * m <= 4096:
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
    if n > m:
        a, b = b, a
        n, m = m, n
    z = 1 << (size - 1).bit_length()
    if n >= 13 and m >= 16384:
        bz = choose_block_ntt(n, m, z)
        if bz:
            return blocked_convolution(a, b, bz)
    if z > 1 << 23:
        raise ValueError("NTT length exceeds 2^23")
    fa = mont_array(a, z)
    plan = ntt_plan(z)
    ntt(fa, False, plan, n)
    if a == b:
        pointwise_square(fa)
    else:
        fb = mont_array(b, z)
        ntt(fb, False, plan, m)
        pointwise(fa, fb)
    ntt(fa, True, plan, 0)
    iz = pow(z, MOD - 2, MOD)
    return finish(fa, size, iz)


def read_ints(data: str) -> list[int]:
    out = list[int]()
    number = 0
    in_number = False
    for char in data:
        c = ord(char)
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


from C import write(int, Ptr[byte], int) -> int

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
    import sys

    values = read_ints(sys.stdin.read())
    n, m = values[0], values[1]
    a = values[2:2 + n]
    b = values[2 + n:2 + n + m]
    write_ints(convolution(a, b))
