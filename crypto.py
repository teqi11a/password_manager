from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Генерация ключа шифрования из мастер-пароля.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


def generate_salt() -> bytes:
    """
    Генерация случайной соли.
    """
    return os.urandom(16)



class PasswordManager:
    def __init__(self, password: str, salt: bytes):
        self.key = derive_key(password, salt)  # Используем переданную соль для генерации ключа
        self.fernet = Fernet(self.key)

    def encrypt_password(self, plain_password: str) -> bytes:
        encrypted_password = self.fernet.encrypt(plain_password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password: bytes, salt: bytes) -> str:
        """
        Дешифруем пароль с использованием соли.
        """
        # Используйте self.key, а не self.key.decode()
        key = derive_key(self.key.decode(), salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_password).decode()
