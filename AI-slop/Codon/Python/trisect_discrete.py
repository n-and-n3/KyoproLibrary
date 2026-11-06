"""Codon port of Python/trisect_discrete.py."""

def trisect_min(array,l=None,r=None,f = lambda x:x):
  ll = 0 if l is None else l
  rr = len(array)-1 if r is None else r
  while rr - ll > 2:
    mid1 = (ll*2+rr)//3
    mid2 = (ll+rr*2)//3
    if f(array[mid1]) >= f(array[mid2]):
      ll = mid1
    else:
      rr = mid2
  return min([f(array[i]) for i in range(ll,rr+1)])


def trisect_max(array,l=None,r=None,f = lambda x:x):
  ll = 0 if l is None else l
  rr = len(array)-1 if r is None else r
  while rr - ll > 2:
    mid1 = (ll*2+rr)//3
    mid2 = (ll+rr*2)//3
    if f(array[mid1]) <= f(array[mid2]):
      ll = mid1
    else:
      rr = mid2
  return max([f(array[i]) for i in range(ll,rr+1)])
