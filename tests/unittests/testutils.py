import sys

if sys.version_info < (3, 0):
    range = xrange


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * int(n / 2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i / 2]:
            sieve[i * i / 2::i] = [False] * ((n - i * i - 1) / (2 * i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n / 2) if sieve[i]]
