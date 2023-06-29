from BitVector import *
import time
AES_modulus = BitVector(bitstring='100011011')
ROUNDS = 14
mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"),
     BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"),
     BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"),
     BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"),
     BitVector(hexstring="01"), BitVector(hexstring="02")]
]

inv_mixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"),
     BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"),
     BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"),
     BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"),
     BitVector(hexstring="09"), BitVector(hexstring="0E")]
]
sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_sbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


def to_hex(state):
    """
    state: list of integers
    """
    return [hex(s)[2:].upper().zfill(2) for s in state]


def print_states(states):
    """
    states: list of 4x4 matrix of bytes
    """
    for matrix in states:
        for row in transpose(matrix):
            print(' '.join(to_hex(row)), end=' ')
        print()

def convert_states_to_hex(states):
    """
    states: list of 4x4 matrix of bytes
    returns: hex string of states
    """
    hex_string = ''
    for matrix in states:
        for row in matrix:
            hex_string += ''.join(to_hex(row))
    return hex_string

def convert_hex_to_states(hex_string):
    """
    hex_string: string of hex values
    returns: list of 4x4 matrix of bytes
    """
    assert len(hex_string) % 32 == 0
    states = [hex_string[i:i+8] for i in range(0, len(hex_string), 8)]
    states = [list(map(lambda x: int(x, 16), [s[i:i+2] for i in range(0, len(s), 2)])) for s in states]
    states = [states[i:i+4] for i in range(0, len(states), 4)]
    return states
    

def g(state, round_key):
    """
    state: tuple of 4 bytes
    round_key: AES round key for key expansion
    """
    temp = state[1:] + state[:1]
    temp = [sbox[t] for t in temp]
    temp[0] = temp[0] ^ round_key
    return temp


def sub_bytes(state, sbox):
    """
    state: 4x4 matrix of bytes
    returns: substituted values for each integer in state
    """
    return [[sbox[i] for i in s] for s in state]


def shift_rows(state):
    """
    state: 4x4 matrix of bytes
    returns: cyclically left shifted rows as per AES specification
    """
    return [s[i:] + s[:i] for i, s in enumerate(state)]


def inv_shift_rows(state):
    """
    state: 4x4 matrix of bytes
    returns: cyclically right shifted rows as per AES specification
    """
    return [s[-i:] + s[:-i] for i, s in enumerate(state)]


def xor(state, round_key):
    """
    state: 4x4 matrix of bytes
    round_key: 4x4 matrix of key for current round
    returns: element-wise XOR of state and round_key
    """
    return [[s ^ r for s, r in zip(s_row, r_row)] for s_row, r_row in zip(state, round_key)]


def mix_column(state, mixer):
    """
    state: 4x4 matrix of bytes
    round_key: 4x4 matrix of key for current round
    returns: galois field matrix multiplication of state and round_key
    """
    assert len(state) == 4
    mixed = [[BitVector(intVal=0, size=8) for _ in range(4)]
             for _ in range(4)]  # 4x4 matrix of 0s
    state = [[BitVector(intVal=s, size=8) for s in i] for i in state]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                mixed[i][j] ^= mixer[i][k].gf_multiply_modular(
                    state[k][j], AES_modulus, 8)
    return [[int(m) for m in i] for i in mixed]


def convert_key_to_bytes(key):
    if key.__class__.__name__ == 'str':
        key_bytes = [ord(c) for c in key]
    elif key.__class__.__name__ == 'int':
        binary = bin(key)[2:].zfill(128)
        assert len(binary) == 128
        key_bytes = [int(binary[i:i+8], 2) for i in range(0, len(binary), 8)]
    return key_bytes


def expand_key(key):
    """
    key: 128 bit key
    returns: list of 44 keys, each key is a list of 4 bytes
    """
    key_bytes = convert_key_to_bytes(key)
    assert len(key_bytes) == 16
    w = [key_bytes[i:i+4] for i in range(0, len(key_bytes), 4)]
    round_key = 1
    for i in range(4, (ROUNDS+1)*4):
        prev = w[i-1]
        if i % 4 == 0:
            prev = g(prev, round_key)
            xor = 0
            if round_key >= 128:
                xor = int("0x11B", 16)
            round_key = (round_key << 1) ^ xor
        w.append(list(map(lambda x, y: x ^ y, w[i-4], prev)))
    return w


def key_expansion_test(key):
    w = expand_key(key)
    for i in range(0, len(w), 4):
        for j in range(4):
            print(" ".join(to_hex(w[i+j])), end=" ")
        print()


def chunk_text(text: str):
    """
    text: string of ASCII characters, 1 byte each
    returns: list of 4x4 byte matrices
    """
    chunks = []
    for i in range(0, len(text), 16):
        if i+16 > len(text):
            chunks.append(text[i:] + (16 - (len(text) - i)) * " ")
        else:
            chunks.append(text[i:i+16])
    chunks = [list(map(ord, c)) for c in chunks]
    return [to_matrix(c) for c in chunks]


def dechunk_text(states):
    """
    states: list of 4x4 byte matrices
    """
    plain = ""
    for matrix in states:
        matrix = transpose(matrix)
        for row in matrix:
            plain += "".join(map(chr, row))
    return plain


def transpose(state):
    return list(map(list, zip(*state)))


def to_matrix(state):
    """
    state: list of 16 bytes
    returns: 4x4 matrix of bytes
    """
    matrix = []
    for i in range(0, len(state), 4):
        matrix.append(state[i:i+4])
    matrix = transpose(matrix)
    return matrix


def aes_rounds(states, keys):
    """
    states: plaintext represented as list of 4x4 byte matrices
    keys: list of 44 keys, each key is a list of 4 bytes
    """
    # initial round
    key = transpose(keys[0:4])
    states = [xor(s, key) for s in states]
    # mid rounds
    for i in range(1, ROUNDS):
        states = [sub_bytes(s, sbox) for s in states]
        states = [shift_rows(s) for s in states]
        states = [mix_column(s, mixer) for s in states]
        key = transpose(keys[4*i:4*(i+1)])
        states = [xor(s, key) for s in states]
    # final round
    states = [sub_bytes(s, sbox) for s in states]
    states = [shift_rows(s) for s in states]
    key = transpose(keys[-4:])
    states = [xor(s, key) for s in states]
    return states


def inverse_aes_rounds(states, keys):
    """
    states: ciphertext represented as list of 4x4 byte matrices
    keys: list of 44 keys, each key is a list of 4 bytes
    """
    # reverse final round
    key = transpose(keys[-4:])
    states = [xor(s, key) for s in states]
    # reverse mid rounds
    for i in range(1, ROUNDS):
        states = [inv_shift_rows(s) for s in states]
        states = [sub_bytes(s, inv_sbox) for s in states]
        key = transpose(keys[-4*(i+1):-4*i])
        states = [xor(s, key) for s in states]
        states = [mix_column(s, inv_mixer) for s in states]
    # reverse initial round
    states = [inv_shift_rows(s) for s in states]
    states = [sub_bytes(s, inv_sbox) for s in states]
    key = transpose(keys[0:4])
    states = [xor(s, key) for s in states]
    return states


def aes_encrypt(text, key):
    """
    text: string of ASCII characters, 1 byte each
    key: string of 16 ASCII characters, 1 byte each
    returns: encrypted hex string
    """
    states = chunk_text(text)
    keys = expand_key(key)
    cipher = aes_rounds(states, keys)
    return convert_states_to_hex(cipher)


def aes_decrypt(cipher, key):
    """
    cipher: encrypted hex string
    key: string of 16 ASCII characters, 1 byte each
    returns: deciphered text
    """
    cipher = convert_hex_to_states(cipher)
    keys = expand_key(key)
    states = inverse_aes_rounds(cipher, keys)
    plain = dechunk_text(states)
    return plain


def aes_encrypt_with_time_details(text, key):
    """
    text: string of ASCII characters, 1 byte each
    key: string of 16 ASCII characters, 1 byte each
    returns: encrypted hex string
    and time takes for key expansion and encryption
    """
    times = {
        "key_expansion": 0,
        "encryption": 0
    }
    states = chunk_text(text)

    tick = time.perf_counter_ns()
    keys = expand_key(key)
    tock = time.perf_counter_ns()
    times["key_expansion"] = (tock - tick) / (10 ** 6)

    tick = time.perf_counter_ns()
    cipher = aes_rounds(states, keys)
    tock = time.perf_counter_ns()
    times["encryption"] = (tock - tick) / (10 ** 6)

    return convert_states_to_hex(cipher), times


def aes_decrypt_with_time_details(cipher, key):
    """
    cipher: encrypted hex string
    key: string of 16 ASCII characters, 1 byte each
    returns: deciphered text and time taken for
    key expansion and decryption
    """
    cipher = convert_hex_to_states(cipher)
    times = {
        "key_expansion": 0,
        "decryption": 0
    }
    tick = time.perf_counter_ns()
    keys = expand_key(key)
    tock = time.perf_counter_ns()
    times["key_expansion"] = (tock - tick) / (10 ** 6)

    tick = time.perf_counter_ns()
    states = inverse_aes_rounds(cipher, keys)
    tock = time.perf_counter_ns()
    times["decryption"] = (tock - tick) / (10 ** 6)

    plain = dechunk_text(states)
    return plain, times


if __name__ == "__main__":
    text = "Can They Do This"
    key = "BUET CSE18 Batch"

    print('-------------------Demo of independent AES implementation------------------\n')
    print("Plain text:")
    print(f"In ASCII: {text}")
    print(f"In HEX: {text.encode('utf-8').hex()}", end='\n\n')

    print("Key:")
    print(f"In ASCII: {key}")
    print(f"In HEX: {key.encode('utf-8').hex()}", end='\n\n')

    cipher, encrypt_times = aes_encrypt_with_time_details(text, key)
    print("Cipher text:")
    print(f"In HEX: {cipher.lower()}")
    cipher_str = ''.join(map(chr, bytes.fromhex(cipher)))
    print(f"In ASCII: {cipher_str}", end='\n\n')

    plain, decrypt_times = aes_decrypt_with_time_details(cipher, key)
    print("Deciphered text:")
    print(f"In HEX: {plain.encode('utf-8').hex()}")
    print(f"In ASCII: {plain}")

    print(f'\n-------------------Execution Time details of AES------------------\n')
    print(f"Key scheduling: {encrypt_times['key_expansion']} ms")
    print(f"Encryption: {encrypt_times['encryption']} ms")
    print(f"Decryption: {decrypt_times['decryption']} ms")
