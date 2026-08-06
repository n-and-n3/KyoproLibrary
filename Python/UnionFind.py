class UnionFind:
	def __init__(self,N):
		self.parent = [-1]*N
		self.next = [i for i in range(N)]
		self.gcnt = N

	def root(self, x):
		r = x
		while self.parent[r] >= 0:
			r = self.parent[r]
		while self.parent[x] >= 0:
			tmp = self.parent[x]
			self.parent[x] = r
			x = tmp
		return r

	def merge(self,x,y):
		fx = self.root(x)
		fy = self.root(y)

		if fx == fy:
			return False

		self.gcnt -= 1
		if self.parent[fx] > self.parent[fy]:
			fx,fy = fy,fx
		# assert xの木のサイズ > yの木のサイズ
		self.parent[fx] += self.parent[fy]
		self.parent[fy] = fx

		self.next[fx], self.next[fy] = self.next[fy], self.next[fx]
		return True

	def same(self,x,y):
		return self.root(x) == self.root(y)

	def comp_size(self,x):
		return -self.parent[self.root(x)]
	
	def size(self):
		return len(self.parent)

	def groupcount(self):
		return self.gcnt

	def comps(self,x):
		p = x
		arr = [x]
		while self.next[p] != x:
			p = self.next[p]
			arr.append(p)
		return arr

	def label(self):
		N = self.size()
		ans = [-1]*N
		c = 0
		for i in range(N):
			if ans[i] != -1:
				continue
			p = i
			ans[i] = c
			while self.next[p] != i:
				p = self.next[p]
				ans[p] = c
			c += 1
		return ans

	def groups(self):
		N = self.size()
		ans = []
		visited = [False]*N
		for i in range(N):
			if visited[i]:
				continue
			p = i
			arr = [i]
			visited[i] = True
			while self.next[p] != i:
				p = self.next[p]
				arr.append(p)
				visited[p] = True
			ans.append(arr)
		return ans
		

# ===========================================================================
def inp():
	return list(map(int,input().split()))
def vout(arr):
	print(" ".join(map(str,arr)))


# https://atcoder.jp/contests/past202203-open/tasks/past202203_h
# https://atcoder.jp/contests/past202203-open/submissions/77732286
def main1():
	N,Q = inp()
	UF = UnionFind(N)
	for _ in range(Q):
		t = inp()
		if t[0] == 1:
			u,v = t[1:]
			u -= 1
			v -= 1
			UF.merge(u,v)
		else:
			v = t[1]
			v -= 1
			arr = [a+1 for a in UF.comps(v)]
			arr.sort()
			vout(arr)

# https://atcoder.jp/contests/atc001/tasks/unionfind_a
# https://atcoder.jp/contests/atc001/submissions/77732375
def main2():
	N,Q = inp()
	UF = UnionFind(N)
	for _ in range(Q):
		p,a,b = inp()
		a -= 1
		b -= 1
		if p == 0:
			UF.merge(a,b)
		else:
			res = UF.same(a,b)
			if res:
				print("Yes")
			else:
				print("No")
		
		
	
N,Q = inp()
UF = UnionFind(N)
for _ in range(Q):
	t = inp()
	if t[0] == 0:
		UF.merge(t[1],t[2])
	elif t[0] == 1:
		print(UF.same(t[1],t[2]))
	elif t[0] == 2:
		print(UF.groups())
	elif t[0] == 3:
		print(UF.label())

"""
5 7
0 0 1
2
0 1 3
2
3
1 3 4
1 0 3
"""

"""
[[0, 1], [2], [3], [4]]
[[0, 3, 1], [2], [4]]
[0, 0, 1, 0, 2]
False
True
"""
