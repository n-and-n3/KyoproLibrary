# cpp/PersistentQueue.cpp declared an empty queue struct. This fills in its
# intended persistent queue API with two shared stacks.
class _QueueStore[T]:
    value: list[T]
    parent: list[int]

    def __init__(self, example: T):
        self.value = []
        self.parent = []

    def node(self, x: T, p: int) -> int:
        i = len(self.value)
        self.value.append(x)
        self.parent.append(p)
        return i


class PersistentQueue[T]:
    store: _QueueStore[T]
    front_head: int
    back_head: int
    front_size: int
    back_size: int

    def __init__(self, example: T):
        self.store = _QueueStore(example)
        self.front_head = -1
        self.back_head = -1
        self.front_size = 0
        self.back_size = 0

    def __init__(self, store: _QueueStore[T], front_head: int, back_head: int, front_size: int, back_size: int):
        self.store = store
        self.front_head = front_head
        self.back_head = back_head
        self.front_size = front_size
        self.back_size = back_size

    def clone(self) -> PersistentQueue[T]:
        return PersistentQueue(self.store, self.front_head, self.back_head, self.front_size, self.back_size)

    def push_back(self, x: T):
        self.back_head = self.store.node(x, self.back_head)
        self.back_size += 1

    def _normalize(self):
        if self.front_head >= 0:
            return
        i = self.back_head
        while i >= 0:
            self.front_head = self.store.node(self.store.value[i], self.front_head)
            self.front_size += 1
            i = self.store.parent[i]
        self.back_head = -1
        self.back_size = 0

    def front(self) -> T:
        self._normalize()
        assert self.front_head >= 0
        return self.store.value[self.front_head]

    def front_or(self, default_value: T) -> T:
        return default_value if self.empty() else self.front()

    def pop_front(self):
        self._normalize()
        assert self.front_head >= 0
        self.front_head = self.store.parent[self.front_head]
        self.front_size -= 1

    def pop_front_safe(self):
        if not self.empty():
            self.pop_front()

    def size(self) -> int:
        return self.front_size + self.back_size

    def empty(self) -> bool:
        return self.size() == 0
