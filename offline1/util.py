import random


def fast_modular_exp(base, exponent, modulus):
    if modulus == 1:
        return 0
    else:
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus
        return result


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def find_coprime(n):
    """
    Returns a number coprime to n
    """
    while True:
        e = random.randint(2, n-1)
        if gcd(e, n) == 1:
            return e


def egcd(a: int, b: int):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def fast_modular_inverse(a, m):
    """
    Returns the modular inverse of a modulo m
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse found")
    return x % m


if __name__ == "__main__":
    from diffie_hellman import *
    import time
    import random

    times = {
        "fast_modular_exp": 0,
        "pow": 0
    }
    for i in range(100000):
        a = random.randint(2**32, 2**64)
        b = random.randint(2**32, 2**64)
        c = random.randint(2**32, 2**64)
        tic = time.perf_counter_ns()
        ans1 = fast_modular_exp(a, b, c)
        toc = time.perf_counter_ns()
        times["fast_modular_exp"] += (toc - tic) / 10**6
        tic = time.perf_counter_ns()
        ans2 = pow(a, b, c)
        toc = time.perf_counter_ns()
        times["pow"] += (toc - tic) / 10**6
        assert ans1 == ans2

    print(times)
