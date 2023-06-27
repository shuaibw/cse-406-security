import random

"""
---------------Diffie-Hellman Key Exchange----------------
In order to factorize a large prime number, I came up with the following algorithm:

1. Generate a large list of 32 bit prime numbers using the miller_rabin test
2. Factors: Randomly sample 4 prime numbers from the list, append 2 to factors
3. Create a test number by multiplying all the factors and adding 1,
   call this number p.
4. Check if p is prime using the miller_rabin test
5. If yes, find a primitive root of p
6. If not, go back to step 2

Explanation:
If p is a prime, then phi(p) = p-1. Since p-1 is a very large number (32*4 bit), 
factorizing it is very difficult. Instead, we can try by going the reverse way.
We first sample 4 32bit prime numbers and multiply them to get a 128 bit number.
Then we add 1 to it and check if it is a prime. If it is a prime, then we already
know the factors of p-1. We can then find a primitive root of p and use it for the
Diffie-Hellman key exchange algorithm. This algorithm is not very efficient, but
it can generate a large prime number in a reasonable amount of time.
"""


def miller_rabin(n, k=20):  # number of tests to run
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    r = 0
    s = n-1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(n):
    """
    Generates a large prime number of n bits
    """
    while 1:
        p = random.randint(2**(n-1), 2**n)
        if miller_rabin(p):
            return p


def find_primitive_root(p, factors):
    """
    p: a large prime number
    factors: list of prime factors of p-1
    Find a primitive root of p
    """
    if p == 2:
        return 1
    phi = p - 1
    while (1):
        g = random.randint(2, p - 1)
        flag = all(pow(g, int(phi / f), p) != 1 for f in factors)
        if flag:
            return g


def find_base_and_modulus(prime_list, key_size, factor_count):
    """
    prime_list: list of prime numbers
    key_size: number of bits in the modulus
    factor_count: number of prime factors to be used from prime_list
    returns: (p, primitive_root) where p is a prime of 
    key_size bits and primitive_root is a primitive root of p
    """
    count = 0
    while True:
        factors = random.sample(prime_list, factor_count)
        factors.append(2)

        p = 1
        for factor in factors:
            p *= factor
        p += 1
        if p.bit_length() != key_size:
            continue
        if miller_rabin(p):
            primitive_root = find_primitive_root(p, factors)
            return p, primitive_root
        count += 1
        if (count % 100000 == 0):
            print("Attempt: ", count)


def generate_modulus_and_base(key_size=128, prime_fct_bit=32, samples=1000):
    """
    key_size: number of bits in the modulus
    prime_fct_bit: number of bits in each prime factor of the modulus
    samples: number of primes of size prime_fct_bit to be generated
    returns: (modulus, base) where modulus is a prime of key_size bits
    and base is a primitive root of modulus
    """
    prime_list = [generate_large_prime(prime_fct_bit) for _ in range(samples)]
    factor_count = key_size // prime_fct_bit
    modulus, base = find_base_and_modulus(prime_list, key_size, factor_count)
    return modulus, base


if __name__ == '__main__':
    modulus, base = generate_modulus_and_base(
        key_size=128, prime_fct_bit=32, samples=1500)
    print("Public Modulus (p):", modulus)
    print("Public Base (g):", base)
    print("Number of bits in p:", modulus.bit_length())
    print("Number of bits in g:", base.bit_length())
