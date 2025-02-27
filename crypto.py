from core.session import Session
from cryptography.fernet import Fernet
import bcrypt
# Генерация и сохранение ключа шифрования
def generate_key():
    key = Fernet.generate_key()
    return key

# Функция хеширования пароля
def hash_password(password: str) -> tuple:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode(), salt


# Функция проверки пароля
def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)

# Функция шифрования паролей сервисов
def encrypt_password(password: str) -> str:
    key = Session.get_user_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

# Функция расшифрования паролей сервисов
def decrypt_password(encrypted_password: str) -> str:
    key = Session.get_user_key()
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password)
    return decrypted_password.decode()
