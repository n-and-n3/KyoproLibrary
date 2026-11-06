class PersistentStack:
    # Shared arrays make clone O(1); each push appends a new immutable node.
    values: list[T]
    parents: list[int]
    pos: int
    size_num: int
    T: type = int

    def __init__(self):
        self.values = []
        self.parents = []
        self.pos = -1
        self.size_num = 0

    def __init__(self, values: list[T]):
        self.values = values[:0]
        self.parents = []
        self.pos = -1
        self.size_num = 0

    def push(self, x: T):
        self.values.append(x)
        self.parents.append(self.pos)
        self.pos = len(self.values) - 1
        self.size_num += 1

    def top(self) -> T:
        assert self.pos >= 0
        return self.values[self.pos]

    def top_or(self, v: T) -> T:
        return v if self.empty() else self.top()

    def pop(self):
        assert self.pos >= 0
        self.pos = self.parents[self.pos]
        self.size_num -= 1

    def pop_safe(self):
        if self.pos >= 0:
            self.pop()

    def empty(self) -> bool:
        return self.pos < 0

    def size(self) -> int:
        return self.size_num

    def clone(self) -> PersistentStack[T]:
        other = PersistentStack(self.values[:0])
        other.values = self.values
        other.parents = self.parents
        other.pos = self.pos
        other.size_num = self.size_num
        return other

    def to_list(self) -> list[T]:
        ans = self.values[:0]
        i = self.pos
        while i >= 0:
            ans.append(self.values[i])
            i = self.parents[i]
        ans.reverse()
        return ans
