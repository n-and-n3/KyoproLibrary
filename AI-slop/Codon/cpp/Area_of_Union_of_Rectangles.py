from bisect import bisect_left


class AreaOfUnionOfRectangles:
    data: list[tuple[int, int, int, int]]
    xs: list[int]
    cnt: list[int]
    cover: list[int]

    def __init__(self, data: list[tuple[int, int, int, int]] = []):
        self.data = data[:]
        self.xs = []
        self.cnt = []
        self.cover = []

    def push(self, a: tuple[int, int, int, int]):
        self.data.append(a)

    def _update(self, i: int, l: int, r: int, ql: int, qr: int, delta: int):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            self.cnt[i] += delta
        else:
            m = (l + r) >> 1
            self._update(i << 1, l, m, ql, qr, delta)
            self._update(i << 1 | 1, m, r, ql, qr, delta)
        if self.cnt[i] > 0:
            self.cover[i] = self.xs[r] - self.xs[l]
        elif r - l == 1:
            self.cover[i] = 0
        else:
            self.cover[i] = self.cover[i << 1] + self.cover[i << 1 | 1]

    def solve(self) -> int:
        events = []
        xs = []
        for x1, y1, x2, y2 in self.data:
            if x1 >= x2 or y1 >= y2:
                continue
            events.append((y1, x1, x2, 1))
            events.append((y2, x1, x2, -1))
            xs.append(x1)
            xs.append(x2)
        if not events:
            return 0
        events.sort()
        self.xs = sorted(set(xs))
        n = len(self.xs) - 1
        self.cnt = [0] * (4 * n + 4)
        self.cover = [0] * (4 * n + 4)
        ans = 0
        previous_y = events[0][0]
        for y, x1, x2, delta in events:
            ans += self.cover[1] * (y - previous_y)
            l = bisect_left(self.xs, x1)
            r = bisect_left(self.xs, x2)
            self._update(1, 0, n, l, r, delta)
            previous_y = y
        return ans
