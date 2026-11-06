class FoldableQueue:
    front_data: list[T]
    back_data: list[T]
    T: type = int

    def __init__(self):
        self.front_data = list[T]()
        self.back_data = list[T]()

    def __init__(self, array: list[T]):
        self.front_data = array[:0]
        self.back_data = array[:]

    def normalized(self):
        if not self.front_data:
            while self.back_data:
                self.front_data.append(self.back_data.pop())

    def check(self) -> bool:
        return len(self.front_data) != 0

    def front(self) -> T:
        self.normalized()
        assert self.front_data
        return self.front_data[-1]

    def front_or(self, default_value: T) -> T:
        return default_value if self.empty() else self.front()

    def push_back(self, x: T):
        self.back_data.append(x)

    def pop_front(self):
        self.normalized()
        assert self.front_data
        self.front_data.pop()

    def pop_front_safe(self):
        if not self.empty():
            self.pop_front()

    def size(self) -> int:
        return len(self.front_data) + len(self.back_data)

    def empty(self) -> bool:
        return self.size() == 0
