"""Functions for encrypting and decrypting the password vault."""

import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# makes a key from the password and the vaults random bytes
def make_key(password, vault_random_bytes):
    # reuse these bytes when opening the vault to get the same key
    key_maker = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=vault_random_bytes,  # salt is the librarys name for these bytes
        iterations=100000,
    )
    key = key_maker.derive(password.encode())
    return base64.urlsafe_b64encode(key)


# turns the data into encrypted bytes for saving
def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data)


# turns the encrypted bytes back into the original data
def decrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.decrypt(data)
