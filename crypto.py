from cryptography.fernet import Fernet
import bcrypt

# Генерация и сохранение ключа шифрования
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Загрузка ключа из файла
def load_key():
    return open("secret.key", "rb").read()

# Функция генерации соли
def generate_salt():
    return bcrypt.gensalt().decode()

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
    key = load_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

# Функция расшифрования паролей сервисов
def decrypt_password(encrypted_password: str) -> str:
    key = load_key()
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password)
    return decrypted_password.decode()
