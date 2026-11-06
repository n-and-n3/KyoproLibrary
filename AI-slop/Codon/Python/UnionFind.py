"""Codon port of Python/UnionFind.py."""

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
