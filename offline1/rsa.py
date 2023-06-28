from util import *
from diffie_hellman import *


def str_to_int(s):
    """
    s: string
    returns: integer representation of s
    """
    return int.from_bytes(s.encode(), 'big')


def int_to_str(i):
    """
    i: integer
    returns: string representation of i
    """
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()


def generate_rsa_key_pairs(n=2048):
    """
    n: number of bits in the public key
    returns: (e, n), (d, n)
    (e,n): public key pair
    (d,n): private key pair
    """
    p = generate_large_prime(n//2)
    q = generate_large_prime(n//2)
    n = p*q
    phi = (p-1)*(q-1)
    e = find_coprime(phi)
    d = fast_modular_inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(m, public_key):
    """
    m: string to be encrypted
    pub: public key pair (e,n)
    returns: encrypted message as integer
    """
    e, n = public_key
    return fast_modular_exp(str_to_int(m), e, n)


def rsa_encrypt_raw(m, public_key):
    e, n = public_key
    return fast_modular_exp(m, e, n)


def rsa_decrypt(c, private_key):
    """
    c: integer to be decrypted
    private_key: private key pair (d,n)
    returns: decrypted message as string
    """
    d, n = private_key
    return int_to_str(fast_modular_exp(c, d, n))


def rsa_decrypt_raw(c, private_key):
    d, n = private_key
    return fast_modular_exp(c, d, n)


if __name__ == "__main__":
    # ------------------ Basic Test ------------------
    # public, private = generate_rsa_key_pairs()
    # msg = "1"
    # cipher = rsa_encrypt(msg, public)
    # print("Cipher: ", cipher)
    # deciphered = rsa_decrypt(cipher, private)
    # print("Deciphered: ", deciphered)
    # ------------------ Basic Test ------------------
    
    # ------------------ Auth Test ------------------
    sender_public, sender_private = generate_rsa_key_pairs()
    receiver_public, receiver_private = generate_rsa_key_pairs()
    msg = "Hello world!"
    cipher = rsa_encrypt(msg, receiver_public)
    signed = rsa_encrypt_raw(cipher, sender_private)
    recieved = signed
    deciphered = rsa_decrypt_raw(recieved, sender_public)
    deciphered = rsa_decrypt(deciphered, receiver_private)
    print(deciphered)
    
    # ------------------ Auth Test ------------------