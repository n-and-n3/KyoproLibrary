"""Codon library form of the two top-level examples in Python/LinearSieve.py.

The returned factor arrays hold indices into primes, as in the source.
"""


def linear_sieve_lpf(N: int):
    primes = list[int]()
    lpf = [-1] * (N + 1)
    for i in range(2, N + 1):
        if lpf[i] == -1:
            lpf[i] = len(primes)
            primes.append(i)
        for j in range(lpf[i] + 1):
            x = i * primes[j]
            if x > N:
                break
            lpf[x] = j
    return primes, lpf


def linear_sieve_mpf(N: int):
    primes = list[int]()
    mpf = [-1] * (N + 1)
    for i in range(2, N + 1):
        if mpf[i] == -1:
            mpf[i] = len(primes)
            primes.append(i)
        for j in range(mpf[i] + 1):
            x = i * primes[j]
            if x > N:
                break
            mpf[x] = mpf[i]
    return primes, mpf
