"""Codon port of Python/NonpopQueue.py."""

class NonpopQueue:
    def __init__(self,array):
        self.array = list(array)
        self.pos = 0

    def append(self,x):
        self.array.append(x)

    def popleft(self):
        if self.pos < len(self.array):
            self.pos += 1
            return self.array[self.pos-1]
        else:
            raise IndexError("pop from empty list")

    def popleft_or(self,defualt):
        if self.pos < len(self.array):
            self.pos += 1
            return self.array[self.pos-1]
        else:
            return defualt

    def __len__(self):
        return len(self.array) - self.pos

    def __getitem__(self,i):
        if 0 <= i <  len(self):
            return self.array[self.pos + i]
        elif -len(self) <= i < 0:
            return self.array[i]
        else:
            raise IndexError("Index out of range")

    def __str__(self):
        return str(self.array[self.pos:])
