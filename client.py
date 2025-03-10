import os
import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

SERVER_URL = "http://127.0.0.1:5000"

# === Fungsi Membuat Akun ===
def create_account(username):
    user_folder = f"users/{username}"
    os.makedirs(user_folder, exist_ok=True)

    key = RSA.generate(2048)

    with open(f"{user_folder}/private.pem", "wb") as f:
        f.write(key.export_key())

    with open(f"{user_folder}/public.pem", "wb") as f:
        f.write(key.publickey().export_key())

    print(f"Akun {username} berhasil dibuat!")

# === Fungsi Memuat Kunci ===
def load_public_key(username):
    try:
        with open(f"users/{username}/public.pem", "rb") as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        print(f"Kunci publik {username} tidak ditemukan!")
        return None

def load_private_key(username):
    try:
        with open(f"users/{username}/private.pem", "rb") as f:
            return RSA.import_key(f.read())
    except FileNotFoundError:
        print(f"Kunci privat {username} tidak ditemukan!")
        return None

# === Fungsi Enkripsi & Dekripsi Pesan ===
def encrypt_message(message, recipient):
    public_key = load_public_key(recipient)
    if public_key is None:
        return None

    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message, username):
    private_key = load_private_key(username)
    if private_key is None:
        return None

    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()

# === Fungsi Kirim & Terima Pesan ===
def send_message(sender, recipient, message):
    encrypted_message = encrypt_message(message, recipient)
    if encrypted_message is None:
        return

    data = {"sender": sender, "recipient": recipient, "message": encrypted_message}
    response = requests.post(f"{SERVER_URL}/send", json=data)
    print(response.json())

def receive_messages(username):
    response = requests.get(f"{SERVER_URL}/receive/{username}")
    messages = response.json()

    if not messages:
        print("Tidak ada pesan baru.")
        return

    for msg in messages:
        decrypted_message = decrypt_message(msg["message"], username)
        print(f"\n📩 Pesan dari {msg['sender']}: {decrypted_message}")

# === Menu Utama ===
def main():
    while True:
        print("\n===== Chat E2EE =====")
        print("1. Buat Akun")
        print("2. Kirim Pesan")
        print("3. Terima Pesan")
        print("4. Keluar")
        choice = input("Pilih menu: ")

        if choice == "1":
            username = input("Masukkan nama pengguna: ")
            create_account(username)

        elif choice == "2":
            sender = input("Nama pengirim: ")
            recipient = input("Nama penerima: ")
            message = input("Masukkan pesan: ")
            send_message(sender, recipient, message)

        elif choice == "3":
            username = input("Masukkan nama pengguna untuk menerima pesan: ")
            receive_messages(username)

        elif choice == "4":
            print("Keluar...")
            break

        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
