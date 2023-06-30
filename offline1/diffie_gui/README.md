# Demonstration of Whole Cryptosystem Using Diffie-Hellman Key Exchange and AES

There are two clients: sender and receiver. At first, a shared secret key is generated using Diffie-Hellman key exchange. Then both sender and receiver use the shared secret key to encrypt and decrypt messages using AES.

## Diffie-Hellman Key Exchange
- First, both clients generate their own secret keys `a` and `b`. The key length field is used to determine the size of this key. The default key length is 128 bits.
- Then either of them generates public modulus `g` and base `p` and shares it with the other client. 
- Finally both clients generate their own public keys $A = g^a \text{ mod }p$ and $A = g^a \text{ mod }p$
- Upon sharing their public keys, both clients can generate the shared secret key $K = B^a \text{ mod }p = A^b \text{ mod }p$.

## Biderectional Messaging using AES
- The shared secret key is used to encrypt and decrypt messages using AES. The default key length of AES is 128 bits. Both sender and receiver use the shared secret key to encrypt and decrypt messages.

## Running the Demo
The following steps are to be followed in order to run the demo:
- Run `python sender.py` to start the sender.
- Run `python receiver.py` in another terminal to start the receiver.
- Generate secret keys for both sender and receiver by pressing the `Generate Secret Key` button.
- Generate modulus and base for either of them by pressing the `Generate Modulus and Base` button.
- Share the modulus and base with the other client.
- Click on `Share Public Key` on both clients to generate and share their public keys.
- Now both clients should automatically generate the shared secret key.
- Type a message in the `Send Text` field and click on `Send Text` button to send the message to the other client.
- The message will be displayed in the `Received Text` field of the other client.
