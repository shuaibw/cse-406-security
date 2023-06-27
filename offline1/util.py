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
        assert ans1==ans2

    print(times)
        
    

