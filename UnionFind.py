# Varified
# https://judge.yosupo.jp/submission/314547

# 神のUnionFind
class UnionFind:
  def __init__(self,N):
    self.parent = [-1]*N

  def union(self,x,y):
    fx = self.find(x)
    fy = self.find(y)
    if fx != fy: # x,y の属する木が異なる
      if self.parent[fx] <= self.parent[fy]: # xの木のサイズ >= yの木のサイズ
        self.parent[fx] += self.parent[fy]
        self.parent[fy] = fx
      else:
        self.parent[fy] += self.parent[fx]
        self.parent[fx] = fy


  def find(self,x):
    f = x
    stack = []
    while self.parent[f] >= 0:
      stack.append(f)
      f = self.parent[f]
    for s in stack:
      self.parent[s] = f
    return f

  def size(self,x):
    return -self.parent[self.find(x)]
