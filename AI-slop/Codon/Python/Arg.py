"""Codon port of Python/Arg.py."""

import math


class Arg:
    def __init__(self, x, y):
        if x == 0 and y == 0:
            raise ValueError("Arg(0,0) is Undefined")
        self.x = x
        self.y = y
        if y < 0:
            self.rank = 0
        elif y == 0 and x > 0:
            self.rank = 1
        elif y > 0:
            self.rank = 2
        else:
            self.rank = 3

    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.x * other.y > other.x * self.y

    def __eq__(self, other):
        return self.rank == other.rank and self.x * other.y == other.x * self.y

    def __le__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.x * other.y >= other.x * self.y

    def __gt__(self, other):
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.x * other.y < other.x * self.y

    def __ge__(self, other):
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.x * other.y <= other.x * self.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_float(self):
        return math.atan2(self.y, self.x)

    def __repr__(self):
        return f"Arg({self.x}, {self.y})"
