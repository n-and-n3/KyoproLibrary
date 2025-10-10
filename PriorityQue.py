# 優先度付きキュー
# https://atcoder.jp/contests/tessoku-book/submissions/69424792

class Heapq:
  def __init__(self,array = None):
    if array != None:
      self.array = [None] + list(sorted(array))
      self.N = len(array)
    else:
      self.array = [None]
      self.N = 0

  def pop(self):
    res = self.array[1]
    self.N -= 1
    if self.N != 0:
      self.array[1] = self.array.pop()
    else:
      self.array.pop()
    p = 1
    while 2*p+1 <= self.N: #子ノード2つともが存在する
      mc = 2*p if self.array[2*p] <= self.array[2*p+1] else 2*p+1
      if self.array[p] > self.array[mc]:
        self.array[p],self.array[mc] = self.array[mc],self.array[p]
        p = mc
      else:
        break
    if 2*p == self.N and self.array[p] > self.array[2*p]: #一人っ子の場合 and 入れ替える必要がある
      self.array[p],self.array[2*p] = self.array[2*p],self.array[p]
    return res
  
  def append(self,x):
    self.array.append(x)
    self.N += 1
    p = self.N
    while p > 1 and self.array[p] < self.array[p//2]:
      self.array[p],self.array[p//2] = self.array[p//2],self.array[p]
      p //= 2
  
  def get(self):
    return self.array[1]

  def __len__(self):
    return self.N
  
  def __bool__(self):
    return len(self) != 0