# Demonstration of Whole Cryptosystem Using RSA Key Exchange and AES

RSA key exchange is used to generate a shared secret key between two clients. Then both clients use the shared secret key to encrypt and decrypt messages using AES.

## RSA Key Exchange
- Sender generates a public key `(e, n)` and a private key `(d, n)` by clicking on the `Generate Key Pairs` button. The size of the key is determined by the `RSA Key Size` field. The default key length is 2048 bits.
- Sender shares the public key `(e, n)` with the receiver.
- Receiver generates a random key `k` and encrypts it using the public key `(e, n)` of the sender. The encrypted key is sent to the sender. The size of the key `k` is determined by the `Secret Key Size` field. The default key length is 128 bits.
- Sender decrypts the encrypted key using its private key `(d, n)` to get the shared secret key `k`.
- Both sender and receiver use the shared secret key `k` to encrypt and decrypt messages using AES. The default key length of AES is 128 bits. Change this by changing the `KEY_SZ` field in `aes.py.`