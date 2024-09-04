import sqlite3
import bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os




conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
session_id = 0
flag = False
user = ""

def create_user(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, master_password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    log_activity(get_session_id(username), "Регистрация")

def authenticate_user(username, master_password):
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        print("Авторизация успешна")
        global session_id, flag, user
        user = username
        session_id = get_session_id(username)
        log_activity(1, "Авторизация")
        flag = True
        return flag
    else:
        print("Неправильное имя пользователя или пароль")

def log_activity(user_id, action):
    c.execute("INSERT INTO activity_logs (user_id, action, username) VALUES (?, ?, ?)", (user_id, action, user))
    conn.commit()

def change_password(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("UPDATE users SET master_password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    log_activity(get_session_id(username), "Смена пароля")


def save_passw(passw, service):
    c.execute("INSERT INTO passwords (user_id, password, service) VALUES (?, ?, ?)", (session_id, service, passw))
    log_activity(get_session_id(user), "Сохранение пароля")
    conn.commit()

def delete_user(username, master_password):
    if not check_user(username, master_password):
        print("Неправильное имя пользователя или пароль")
    else:
        user_id = get_session_id(username)
        if user_id is not None:
            c.execute("DELETE FROM users WHERE username = ?", (username,))
            c.execute("DELETE FROM passwords WHERE user_id = ?", (user_id,))
            log_activity(1, "Удаление аккаунта")
            conn.commit()
        else:
            print("User not found")


def check_user(username, master_password):
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        return True
    else:
        print("Неправильное имя пользователя или пароль")

def get_session_id(username):
    try:
        __user_id = c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        return __user_id
    except Exception as e:
        print(f"Error: {e}")
        return None


def logout() -> bool:
    global session_id, flag, user
    log_activity(get_session_id(user), "Выход")
    session_id = 0
    flag = False
    user = ""
    print("Вы вышли из аккаунта")
    return flag



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


    def __init__(self, master_password: str, salt: bytes):
        self.key = derive_key(master_password, salt)
        self.fernet = Fernet(self.key)


    def encrypt_password(self, plain_password: str) -> bytes:
        return self.fernet.encrypt(plain_password.encode())


    def decrypt_password(self, encrypted_password: bytes) -> str:
        return self.fernet.decrypt(encrypted_password).decode()
