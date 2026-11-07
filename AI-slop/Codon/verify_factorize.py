"""Run with Codon 0.19.3: codon run -release verify_factorize.py."""

from factorize import is_prime, factorize, _miller_rabin
from is_prime_fast import is_prime as is_prime_fast


def trial(n: int) -> list[int]:
    result: list[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            result.append(d)
            n //= d
        d += 1
    if n > 1:
        result.append(n)
    return result


for n in range(1, 2001):
    expected = trial(n)
    assert factorize(n) == expected
    assert is_prime(n) == (len(expected) == 1 and expected[0] == n)
    assert is_prime_fast(n) == is_prime(n)

assert is_prime(941647938162115519)
assert is_prime_fast(941647938162115519)
assert is_prime_fast(4294967291)
assert not is_prime_fast(4294967297)
assert factorize(4294967297) == [641, 6700417]
assert _miller_rabin(5461, True) == 127
assert factorize(5461) == [43, 127]
assert factorize(999381247093216751) == [999665081, 999716071]
assert factorize(999999967571071807) == [364440383, 2743932929]
assert factorize(341550071728321) == [10670053, 32010157]
assert factorize(10**18) == [2] * 18 + [5] * 18

print("number theory self-check OK")
