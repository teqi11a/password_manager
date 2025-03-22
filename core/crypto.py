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
    """
    Создает производный ключ шифрования на основе мастер-пароля и соли.

    Используется алгоритм PBKDF2HMAC с SHA-256 для создания ключа фиксированной длины.
    Этот ключ будет использоваться как базовый для генерации основного ключа шифрования.

    Args:
        master_password (str): Мастер-пароль пользователя.
        salt (bytes): Соль для усиления безопасности ключа.

    Returns:
        bytes: Производный ключ шифрования.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=kdf_conf['AES_KEY_LENGTH'],
        salt=salt,
        iterations=kdf_conf['KDF_ITERATIONS'],
    )
    return kdf.derive(master_password.encode())


def generate_encrypted_key(master_password: str) -> tuple:
    """
    Генерирует основной ключ шифрования для пользователя и шифрует его.

    Использует случайную соль, мастер-пароль и производный ключ для создания
    зашифрованного ключа, который может быть безопасно сохранен в базе данных.

    Args:
        master_password (str): Мастер-пароль пользователя.

    Returns:
        tuple: Кортеж из двух элементов:
            - kdf_salt (str): Соль, закодированная в base64.
            - encrypted_key (str): Зашифрованный ключ шифрования.
    """
    # Генерируем соль для KDF
    kdf_salt = os.urandom(kdf_conf['KDF_SALT_SIZE'])

    # Производный ключ для шифрования
    derived_key = derive_key(master_password, kdf_salt)

    # Генерируем и шифруем Fernet-ключ
    fernet_key = Fernet.generate_key()
    cipher = Fernet(base64.urlsafe_b64encode(derived_key))
    encrypted_key = cipher.encrypt(fernet_key)

    # Возвращаем кортеж с солью и ключом шифрования для записи в базу
    return (
        base64.b64encode(kdf_salt).decode(),
        encrypted_key.decode()
    )


def decrypt_user_key(master_password: str, kdf_salt: str, encrypted_key: str) -> bytes:
    """
    Расшифровывает зашифрованный ключ шифрования, используя мастер-пароль и соль.

    Args:
        master_password (str): Мастер-пароль пользователя.
        kdf_salt (str): Соль, закодированная в base64.
        encrypted_key (str): Зашифрованный ключ шифрования.

    Returns:
        bytes: Расшифрованный ключ шифрования.
    """
    salt = base64.b64decode(kdf_salt)
    derived_key = derive_key(master_password, salt)

    cipher = Fernet(base64.urlsafe_b64encode(derived_key))
    return cipher.decrypt(encrypted_key.encode())



def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.

    Args:
        password (str): Пароль, который нужно хэшировать.

    Returns:
        str: Хэшированный пароль в виде строки.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли пароль хэшированному паролю.

    Args:
        password (str): Пароль для проверки.
        hashed_password (str): Хэшированный пароль для сравнения.

    Returns:
        bool: True, если пароль совпадает с хэшированным паролем, иначе False.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def encrypt_password(data: str, key: bytes) -> str:
    """
    Шифрует данные (например, пароль) с использованием ключа Fernet.

    Args:
        data (str): Данные, которые нужно зашифровать.
        key (bytes): Ключ шифрования.

    Returns:
        str: Зашифрованные данные в виде строки.
    """
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode()


def decrypt_password(encrypted_data: str, key: bytes) -> str:
    """
    Расшифровывает данные (например, пароль) с использованием ключа Fernet.

    Args:
        encrypted_data (str): Зашифрованные данные.
        key (bytes): Ключ шифрования.

    Returns:
        str: Расшифрованные данные в виде строки.
    """
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data.encode()).decode()