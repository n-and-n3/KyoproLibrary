class MergeSortTree:
    def __init__(self, _array):
        self.sz = len(_array)
        self.N = 1
        while self.N < self.sz:
            self.N *= 2
        self.array = [[]]*(2*self.N)
        for i in range(self.sz):
            self.array[self.N+i] = [_array[i]]
        for i in range(self.N-1,0,-1):
            self.array[i] = self._merge(self.array[2*i], self.array[2*i+1])
    
    def count_lt(self,l,r,c):
        l += self.N
        r += self.N
        res = 0
        while r - l > 0:
            if r & 1:
                r -= 1
                res += self._count_lt(self.array[r], c)
            if l & 1:
                res += self._count_lt(self.array[l], c)
                l += 1
            l >>= 1
            r >>= 1
        return res
    
    
    def _merge(self,X,Y):
        res = []
        i = 0
        j = 0
        while i < len(X) and j < len(Y):
            if X[i] <= Y[j]:
                res.append(X[i])
                i += 1
            else:
                res.append(Y[j])
                j += 1
        while i < len(X):
            res.append(X[i])
            i += 1
        while j < len(Y):
            res.append(Y[j])
            j += 1
        return res

    def _count_lt(self,arr,x): # arr の中で x 未満のものの個数
        # x 以上最小のインデックスを返す
        ng = 0
        ok = len(arr)
        if len(arr) == 0 or arr[0] >= x:
            return 0
        while ok - ng > 1:
            mid = (ok+ng+1)//2
            if arr[mid] >= x:
                ok = mid
            else:
                ng = mid
        return ok

    
    def __len__(self):
        return self.sz


MST = MergeSortTree([5,4,7,3,2,1,0,6])

for arr in MST.array:
    print(arr)

print(MST.count_lt(0,6,0))
print(MST.count_lt(0,6,1))
print(MST.count_lt(0,6,2))
print(MST.count_lt(0,6,3))
print(MST.count_lt(0,6,4))
print(MST.count_lt(0,6,5))
print(MST.count_lt(0,6,6))
print(MST.count_lt(0,6,7))
print(MST.count_lt(0,6,8))









