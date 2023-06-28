import random
from util import *
import time
from prettytable import PrettyTable


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

MIN = 2**64
MAX = 2**128


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
        x = fast_modular_exp(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = fast_modular_exp(x, 2, n)
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
        g = random.randint(MIN, MAX)  # primitive root candidate
        flag = all(fast_modular_exp(g, int(phi / f), p) != 1 for f in factors)
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


def generate_modulus_and_base(key_size=128, prime_fct_bit=32, samples=1000, min=2**64, max=2**128):
    """
    key_size: number of bits in the modulus
    prime_fct_bit: number of bits in each prime factor of the modulus
    samples: number of primes of size prime_fct_bit to be generated
    returns: (modulus, base) where modulus is a prime of key_size bits
    min, max: range of the candidate primitive roots
    and base is a primitive root of modulus
    """
    assert key_size % prime_fct_bit == 0
    assert min < max <= 2**key_size
    MIN = min
    MAX = max
    prime_list = [generate_large_prime(prime_fct_bit) for _ in range(samples)]
    factor_count = key_size // prime_fct_bit  # number of prime factors to be used in the modulus
    modulus, base = find_base_and_modulus(prime_list, key_size, factor_count)
    return modulus, base


def generate_public_key(modulus, base, private):
    """
    modulus: key_size bit prime number
    base: primitive root of modulus
    private: secret key for each party
    returns: base^private mod modulus
    """
    return fast_modular_exp(base, private, modulus)


def generate_shared_secret(modulus, public_key, private):
    """
    modulus: key_size bit prime number
    public_key: public key of the other party
    private: secret key for each party
    returns: public_key^private mod modulus
    """
    return fast_modular_exp(public_key, private, modulus)


def __find_base(prime_list, key_size, factor_count):
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
            return p, factors
        count += 1
        if (count % 100000 == 0):
            print("Attempt: ", count)


def __run_test(key_sizes, prime_fct_bit, prime_list, min, max, iter=10):
    MIN = min
    MAX = max
    times = {
        128: {
            'p': 0,
            'g': 0,
            'a': 0,
            'A': 0,
            'secret': 0
        },
        192: {
            'p': 0,
            'g': 0,
            'a': 0,
            'A': 0,
            'secret': 0
        },
        256: {
            'p': 0,
            'g': 0,
            'a': 0,
            'A': 0,
            'secret': 0
        }
    }
    for _ in range(iter):
        print('Iteration: ', _)
        for k in key_sizes:
            print(f'Running test for Key size: {k}')
            tic = time.perf_counter_ns()
            p, factors = __find_base(prime_list, k, k//prime_fct_bit)
            toc = time.perf_counter_ns()
            times[k]['p'] += (toc-tic)/10**6

            tic = time.perf_counter_ns()
            modulus = find_primitive_root(p, factors)
            toc = time.perf_counter_ns()
            times[k]['g'] += (toc-tic)/10**6

            tic = time.perf_counter_ns()
            a = generate_large_prime(k)
            toc = time.perf_counter_ns()
            times[k]['a'] += (toc-tic)/10**6

            b = generate_large_prime(k)

            tic = time.perf_counter_ns()
            A = fast_modular_exp(modulus, a, p)
            toc = time.perf_counter_ns()
            times[k]['A'] += (toc-tic)/10**6

            B = fast_modular_exp(modulus, b, p)

            tic = time.perf_counter_ns()
            secret_A = fast_modular_exp(B, a, p)
            toc = time.perf_counter_ns()
            times[k]['secret'] += (toc-tic)/10**6

            secret_B = fast_modular_exp(A, b, p)
            assert secret_A == secret_B
    return times


if __name__ == '__main__':
    # ----------------- Testing -----------------
    # modulus, base = generate_modulus_and_base(
    #     key_size=128, prime_fct_bit=32, samples=1500, min=2**64, max=2**128)
    # print("Public Modulus (p):", modulus)
    # print("Public Base (g):", base)
    # print("Number of bits in p:", modulus.bit_length())
    # print("Number of bits in g:", base.bit_length())

    # sender_private = generate_large_prime(128)
    # receiver_private = generate_large_prime(128)
    # sender_public = generate_public_key(modulus, base, sender_private)
    # receiver_public = generate_public_key(modulus, base, receiver_private)
    # sender_shared_secret = generate_shared_secret(modulus, receiver_public, sender_private)
    # receiver_shared_secret = generate_shared_secret(modulus, sender_public, receiver_private)
    # print("Sender's shared secret:", sender_shared_secret)
    # print("Receiver's shared secret:", receiver_shared_secret)
    # ----------------- Testing -----------------
    key_sizes = [128, 192, 256]
    iter = 20
    primes = [generate_large_prime(32) for _ in range(2500)]
    times = __run_test(key_sizes, 32, primes, 2**64, 2**128, iter)
    table = PrettyTable()
    table.field_names = ["Key Size", "p", "g", "a", "A", "Secret"]
    for k, v in times.items():
        p = "{:.5f}".format(v['p']/iter)
        g = "{:.5f}".format(v['g']/iter)
        a = "{:.5f}".format(v['a']/iter)
        A = "{:.5f}".format(v['A']/iter)
        secret = "{:.5f}".format(v['secret']/iter)
        table.add_row([k, p, g, a, A, secret])
    print(table)
