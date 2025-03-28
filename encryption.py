from cryptography.fernet import Fernet
import os

# ✅ Function to generate & save encryption key
def generate_key():
    """Generates and saves a new encryption key if 'secret.key' does not exist."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# ✅ Function to load encryption key
def load_key():
    """Loads the encryption key from 'secret.key'. Generates a new one if missing."""
    if not os.path.exists("secret.key"):
        generate_key()
    return open("secret.key", "rb").read()

# ✅ Encrypt Password
def encrypt_password(password):
    """Encrypts a password using the stored encryption key."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()

# ✅ Decrypt Password
def decrypt_password(encrypted_password):
    """Decrypts an encrypted password using the stored encryption key."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()
