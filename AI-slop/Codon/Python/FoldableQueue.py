"""Codon port of Python/FoldableQueue.py."""

class FoldableQueue:
    def __init__(self,array):
        self.rear = list(array)
        self.front = self.rear[:0]

    def append(self,x):
        self.rear.append(x)

    def popleft(self):
        if self.front:
            return self.front.pop()
        elif self.rear:
            self.normarize()
            return self.front.pop()
        else:
            raise IndexError("pop from empty list")

    def popleft_or(self,defualt):
        if self.front:
            return self.front.pop()
        elif self.rear:
            self.normarize()
            return self.front.pop()
        else:
            return defualt

    def normarize(self):
        while self.rear:
            self.front.append(self.rear.pop())

    def __len__(self):
        return len(self.front) + len(self.rear)

    def __getitem__(self,i):
        if 0 <= i <  len(self):
            if i < len(self.front):
                return self.front[~i]
            else:
                return self.rear[i-len(self.front)]
        elif -len(self) <= i < 0:
            if -len(self.rear) <= i:
                return self.rear[i]
            else:
                return self.front[~(i+len(self.rear))]
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return str(list(reversed(self.front))+self.rear)
