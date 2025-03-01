from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import bcrypt
import os
import base64

# Конфигурация KDF
kdf_conf = {
    'KDF_ITERATIONS' : 480000,
    'KDF_SALT_SIZE' : 16,
    'AES_KEY_LENGTH' : 32
}


def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=kdf_conf['AES_KEY_LENGTH'],
        salt=salt,
        iterations=kdf_conf['KDF_ITERATIONS'],
    )
    return kdf.derive(master_password.encode())


# Генерация ключа шифрования используя мастер-пароль и сохраненную соль
def generate_encrypted_key(master_password: str) -> tuple:

    # Генерируем соль для KDF
    kdf_salt = os.urandom(kdf_conf['KDF_SALT_SIZE'])

    # Производный ключ для шифрования
    derived_key = derive_key(master_password, kdf_salt)

    # Генерируем и шифруем Fernet-ключ
    fernet_key = Fernet.generate_key()
    cipher = Fernet(base64.urlsafe_b64encode(derived_key))
    encrypted_key = cipher.encrypt(fernet_key)

    return (
        base64.b64encode(kdf_salt).decode(),
        encrypted_key.decode()
    )


def decrypt_user_key(master_password: str, kdf_salt: str, encrypted_key: str) -> bytes:
    salt = base64.b64decode(kdf_salt)
    derived_key = derive_key(master_password, salt)

    cipher = Fernet(base64.urlsafe_b64encode(derived_key))
    return cipher.decrypt(encrypted_key.encode())


# Оригинальные функции с доработками

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def encrypt_password(data: str, key: bytes) -> str:
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode()


def decrypt_password(encrypted_data: str, key: bytes) -> str:
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data.encode()).decode()