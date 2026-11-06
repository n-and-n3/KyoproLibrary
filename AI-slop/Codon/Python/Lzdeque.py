"""Codon port of Python/Lzdeque.py."""

from collections import deque


class Lzdeque:
  deque: deque[tuple[T,int]]
  indexdeque: deque[int]
  length: int
  T: type = int

  def __init__(self):
    self.deque = deque[tuple[T,int]]()
    self.indexdeque = deque([0])
    self.length = 0

  def __init__(self,array: list[tuple[T,int]]):
    self.deque = deque(array)
    self.indexdeque = deque([0])
    for i in range(len(array)):
      self.indexdeque.append(self.indexdeque[-1] + array[i][1])
    self.length = sum(x[1] for x in array)

  def pop(self,k):
    if self.length < k:
      raise IndexError("pop from an empty Lzdeque")
    self.length -= k
    ans = []
    s = 0
    while s < k:
      v,c = self.deque.pop()
      self.indexdeque.pop()
      ans.append((v,c))
      s += c
    d = s - k
    if d > 0:
      ans[-1] = (ans[-1][0], ans[-1][1] - d)
      self.deque.append((ans[-1][0], d))
      self.indexdeque.append(self.indexdeque[-1] + d)
    return ans

  def append(self,x,k):
    self.length += k
    if len(self.deque) != 0 and self.deque[-1][0] == x:
      v,c = self.deque.pop()
      self.deque.append((x,c+k))
      last = self.indexdeque.pop()
      self.indexdeque.append(last+k)
    else:
      self.deque.append((x,k))
      self.indexdeque.append(self.indexdeque[-1] + k)

  def popleft(self,k):
    if self.length < k:
      raise IndexError("popleft from an empty Lzdeque")
    self.length -= k
    ans = []
    s = 0
    while s < k:
      v,c = self.deque.popleft()
      self.indexdeque.popleft()
      ans.append((v,c))
      s += c
    d = s - k
    if d > 0:
      ans[-1] = (ans[-1][0], ans[-1][1] - d)
      self.deque.appendleft((ans[-1][0], d))
      self.indexdeque.appendleft(self.indexdeque[0] - d)
    return ans

  def appendleft(self,x,k):
    self.length += k
    if len(self.deque) != 0 and self.deque[0][0] == x:
      v,c = self.deque.popleft()
      self.deque.appendleft((x,c+k))
      first = self.indexdeque.popleft()
      self.indexdeque.appendleft(first-k)
    else:
      self.deque.appendleft((x,k))
      self.indexdeque.appendleft(self.indexdeque[0] - k)

  def __len__(self):
    return self.length

  def __bool__(self):
    return self.length != 0

  # ランダムアクセスする関数 [] ← どうやるんだっけ？
  # 負番の場合どうする？というかtatyamSetってキーが小さいときは高速に動くんだっけか
  # どうやって実装してるんだ？ちょっと実装見よう...
  # あ～なるほど、平方分割だからブロック単位の探索に線形探索でO(√N)掛かっていいのか
  # え～Pythonならランダムアクセスの速度一定？
  # ん～～～～
  # iがある程度小さいときは線形探索させるか？
  # やめよう、汚いし余計なifあるべきではない
  # どうしても気になるなら、線形探索をする別の関数 get 関数を実装すべきかも ← そうするか

  def __getitem__(self, i):
    if i < 0:
      i += self.length
    offset = self.indexdeque[0]
    if i < 0 or i >= self.length:
      raise IndexError("Lzdeque index out of range")
    target = i + offset
    lo, hi = 0, len(self.indexdeque)
    while lo < hi:
      mid = (lo + hi) >> 1
      if self.indexdeque[mid] <= target:
        lo = mid + 1
      else:
        hi = mid
    return self.deque[lo - 1][0]

  def __iter__(self):
    for i in range(len(self.deque)):
      c = self.deque[i][0]
      for j in range(self.deque[i][1]):
        yield c

  def __str__(self):
    return str(self.deque)
