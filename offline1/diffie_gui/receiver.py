import sys
sys.path.append('..')
import tkinter as tk
import socket
import threading
from aes import *
from diffie_hellman import *


class SenderClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Receiver Client")
        self.master.geometry("750x320")  # Set window size

        # Add labels
        tk.Label(master, text="Send Text:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Receive Text:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Shared secret:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Public Modulus:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Public Base:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Secret Key:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
        tk.Label(master, text="Public Key:").grid(row=6, column=0, sticky='e', padx=5, pady=5)

        self.send_text = tk.Entry(master, width=50)
        self.receive_text = tk.Entry(master, width=50)
        self.shared_secret = tk.Entry(master, width=50)
        self.public_modulus = tk.Entry(master, width=50)
        self.public_base = tk.Entry(master, width=50)
        self.secret_key = tk.Entry(master, width=50)
        self.public_key = tk.Entry(master, width=50)

        self.f1 = tk.Frame(master)
        tk.Label(self.f1, text="Key Size:").pack(side=tk.LEFT, padx=5, pady=5)
        self.key_size = tk.Entry(self.f1, width=4)
        self.key_size.pack(side=tk.LEFT, padx=5, pady=5)

        self.send_text.grid(row=0, column=1, padx=5, pady=5)
        self.receive_text.grid(row=1, column=1, padx=5, pady=5)
        self.shared_secret.grid(row=2, column=1, padx=5, pady=5)
        self.public_modulus.grid(row=3, column=1, padx=5, pady=5)
        self.public_base.grid(row=4, column=1, padx=5, pady=5)
        self.secret_key.grid(row=5, column=1, padx=5, pady=5)
        self.public_key.grid(row=6, column=1, padx=5, pady=5)
        self.f1.grid(row=1, column=2, padx=5, pady=5)

        self.generate_key_button = tk.Button(
            master, text="Generate Secret Key", command=self.generate_key)
        self.generate_mod_base_button = tk.Button(
            master, text="Generate Modulus and Base", command=self.generate_mod_base)
        self.share_mod_base_button = tk.Button(
            master, text="Share Modulus and Base", command=self.share_mod_base)
        self.send_text_button = tk.Button(master, text="Send Text", command=self.send_text_message)
        self.share_public_key_button = tk.Button(
            master, text="Share Public Key", command=self.share_public_key)

        self.generate_key_button.grid(row=2, column=2, padx=5, pady=5)
        self.generate_mod_base_button.grid(row=3, column=2, padx=5, pady=5)
        self.share_mod_base_button.grid(row=4, column=2, padx=5, pady=5)
        self.send_text_button.grid(row=0, column=2, padx=5, pady=5)
        self.share_public_key_button.grid(row=6, column=2, padx=5, pady=5)

        self.key_size.insert(0, "128")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 12345))

        thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        thread.start()

    def generate_key(self):
        # Placeholder function
        self.secret_key.delete(0, tk.END)
        bits = int(self.key_size.get())
        if bits > 128:
            bits = bits//2
        self.secret_key.insert(0, generate_large_prime(bits))

    def generate_mod_base(self):
        # Placeholder function
        k_sz = int(self.key_size.get())
        modulus, base = generate_modulus_and_base(key_size=k_sz)
        self.public_modulus.delete(0, tk.END)
        self.public_modulus.insert(0, str(modulus))
        self.public_base.delete(0, tk.END)
        self.public_base.insert(0, str(base))

    def share_mod_base(self):
        # Placeholder function
        message = f"m{self.public_modulus.get()},{self.public_base.get()}"
        self.sock.sendall(message.encode())

    def share_public_key(self):
        pub_key = generate_public_key(
            int(self.public_modulus.get()), int(self.public_base.get()), int(self.secret_key.get()))
        self.public_key.delete(0, tk.END)
        self.public_key.insert(0, str(pub_key))
        self.sock.sendall(f"k{pub_key}".encode())

    def send_text_message(self):
        message = self.send_text.get()
        cipher = 't' + aes_encrypt(message, int(self.shared_secret.get()))
        self.sock.sendall(cipher.encode())

    def listen_for_messages(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                # Handle received data here
                s = data.decode()
                if s[0] == 'm':  # modulus,base
                    pieces = s[1:].split(',')
                    modulus = pieces[0]
                    base = pieces[1]
                    self.public_modulus.delete(0, tk.END)
                    self.public_modulus.insert(0, modulus)
                    self.public_base.delete(0, tk.END)
                    self.public_base.insert(0, base)
                elif s[0] == 'k':  # public key
                    public_key = int(s[1:])
                    print(f"Public key from sender: {public_key}")
                    secret = generate_shared_secret(
                        int(self.public_modulus.get()), public_key, int(self.secret_key.get()))
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
