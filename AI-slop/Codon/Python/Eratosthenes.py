"""Codon port of Python/Eratosthenes.py."""

def Eratosthenes(n):
	table = [True]*(n+1)
	primes = []

	table[0] = False
	if n >= 1:
		table[1] = False

	for i in range(2,n+1):
		if table[i]:
			primes.append(i)
			for j in range(2*i,n+1,i):
				table[j] = False

	return table, primes
