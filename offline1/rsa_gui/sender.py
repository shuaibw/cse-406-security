import sys
sys.path.append('..')
import tkinter as tk
import socket
import threading
from aes import *
from rsa import *
from diffie_hellman import *


class SenderClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Sender Client")
        self.master.geometry("750x320")  # Set window size

        # Add labels
        tk.Label(master, text="Send Text:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Receive Text:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Shared secret:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Public Key:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Private Key:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Modulo:").grid(row=5, column=0, sticky='e', padx=5, pady=5)

        self.send_text = tk.Entry(master, width=50)
        self.receive_text = tk.Entry(master, width=50)
        self.shared_secret = tk.Entry(master, width=50)
        self.public_key = tk.Entry(master, width=50)
        self.private_key = tk.Entry(master, width=50)
        self.modulo = tk.Entry(master, width=50)

        self.f1 = tk.Frame(master)
        tk.Label(self.f1, text="Secret Key Size:").pack(side=tk.LEFT, padx=5, pady=5)
        self.key_size = tk.Entry(self.f1, width=4)
        self.key_size.pack(side=tk.LEFT, padx=5, pady=5)
        self.f2 = tk.Frame(master)
        tk.Label(self.f2, text="RSA Key Size:").pack(side=tk.LEFT, padx=5, pady=5)
        self.rsa_key_size = tk.Entry(self.f2, width=5)
        self.rsa_key_size.pack(side=tk.LEFT, padx=5, pady=5)

        self.send_text.grid(row=0, column=1, padx=5, pady=5)
        self.receive_text.grid(row=1, column=1, padx=5, pady=5)
        self.shared_secret.grid(row=2, column=1, padx=5, pady=5)
        self.public_key.grid(row=3, column=1, padx=5, pady=5)
        self.private_key.grid(row=4, column=1, padx=5, pady=5)
        self.modulo.grid(row=5, column=1, padx=5, pady=5)

        self.generate_secret_button = tk.Button(
            master, text="Generate Secret Key", command=self.generate_secret_key, state=tk.DISABLED)
        self.generate_key_pairs_button = tk.Button(
            master, text="Generate Key Pairs", command=self.generate_key_pairs)
        self.share_public_button = tk.Button(
            master, text="Share Public Key", command=self.share_public_key)
        self.send_text_button = tk.Button(master, text="Send Text", command=self.send_text_message)
        self.exchange_secret_button = tk.Button(
            master, text="Exchange Secret", command=self.exchange_secret, state = tk.DISABLED)

        self.send_text_button.grid(row=0, column=2, padx=5, pady=5)
        self.f1.grid(row=1, column=2, padx=5, pady=5)
        self.generate_secret_button.grid(row=2, column=2, padx=5, pady=5)
        self.generate_key_pairs_button.grid(row=3, column=2, padx=5, pady=5)
        self.share_public_button.grid(row=4, column=2, padx=5, pady=5)
        self.f2.grid(row=5, column=2, padx=5, pady=5)
        self.exchange_secret_button.grid(row=6, column=2, padx=5, pady=5)

        self.key_size.insert(0, "128")
        self.rsa_key_size.insert(0, "2048")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 12345))
        self.c = None

        thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        thread.start()

    def generate_secret_key(self):
        # Placeholder function
        self.shared_secret.delete(0, tk.END)
        bits = int(self.key_size.get())
        self.shared_secret.insert(0, generate_large_prime(bits))

    def generate_key_pairs(self):
        # Placeholder function
        rsa_key_size = int(self.rsa_key_size.get())
        public_key, private_key = generate_rsa_key_pairs(rsa_key_size)
        e, n = public_key
        d, n = private_key
        self.public_key.delete(0, tk.END)
        self.public_key.insert(0, str(e))
        self.private_key.delete(0, tk.END)
        self.private_key.insert(0, str(d))
        self.modulo.delete(0, tk.END)
        self.modulo.insert(0, str(n))

    def share_public_key(self):
        # Placeholder function
        message = f"m{self.public_key.get()},{self.modulo.get()}"
        self.c.sendall(message.encode())

    def exchange_secret(self):
        secret = self.shared_secret.get()
        e, n = int(self.public_key.get()), int(self.modulo.get())
        encrypted = rsa_encrypt(secret, (e, n))
        self.c.sendall(f"k{encrypted}".encode())

    def send_text_message(self):
        message = self.send_text.get()
        cipher = 't' + aes_encrypt(message, int(self.shared_secret.get()))
        self.c.sendall(cipher.encode())

    def listen_for_messages(self):
        self.sock.listen(1)
        c, addr = self.sock.accept()
        self.c = c
        print("Connection from: " + str(addr))
        while True:
            data = self.c.recv(4096)
            if data:
                # Handle received data here
                s = data.decode()
                if s[0] == 'm':  # (e,n) public key
                    pieces = s[1:].split(',')
                    e = pieces[0]
                    n = pieces[1]
                    self.public_key.delete(0, tk.END)
                    self.public_key.insert(0, e)
                    self.modulo.delete(0, tk.END)
                    self.modulo.insert(0, n)
                elif s[0] == 'k':  # secret key
                    public_key = int(s[1:])
                    print(f"Encrypted Secret key from reciever: {public_key}")
                    d, n = int(self.private_key.get()), int(self.modulo.get())
                    secret = rsa_decrypt(public_key, (d, n))
                    self.shared_secret.delete(0, tk.END)
                    self.shared_secret.insert(0, secret)
                elif s[0] == 't':  # encrypted text
                    encrypted_text = s[1:]
                    print(f"Received encrypted text: {encrypted_text}")
                    decrypted = aes_decrypt(encrypted_text, int(self.shared_secret.get()))
                    self.receive_text.delete(0, tk.END)
                    self.receive_text.insert(0, decrypted)
                else:
                    print(f"Received: {s}")


root = tk.Tk()
my_gui = SenderClient(root)
root.mainloop()
