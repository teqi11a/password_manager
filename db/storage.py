import sqlite3
from core import crypto
from translation import Language
from i18n import t
from core.crypto import (
    hash_password,
    check_password,
    encrypt_password,
    decrypt_password,
    generate_encrypted_key,
    decrypt_user_key
)

conn = sqlite3.connect('password_manager.db', check_same_thread=False)


class Session:
    _current_user = None
    _fernet_key = None
    _auth_flag = False

    @classmethod
    def initialize(cls, user_id: int, username: str, fernet_key: bytes | None):
        cls._current_user = {'id': user_id, 'username': username}
        cls._fernet_key = fernet_key
        cls._auth_flag = True  # Устанавливаем флаг при авторизации

    @classmethod
    def clear(cls):
        cls._current_user = None
        # Безопасное удаление ключа из памяти
        if cls._fernet_key:
            cls._fernet_key = b'\x00' * len(cls._fernet_key)
        cls._auth_flag = False  # Сбрасываем флаг при выходе

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._auth_flag  # Метод для проверки состояния авторизации

    @classmethod
    def get_user_id(cls):
        return cls._current_user['id'] if cls._current_user else None

    @classmethod
    def get_fernet_key(cls):
        return cls._fernet_key

class AuthService:
    @staticmethod
    def register(username: str, master_password: str) -> bool:
        try:
            kdf_salt, encrypted_key = generate_encrypted_key(master_password)
            hashed_password = hash_password(master_password)

            with conn:
                cur = conn.execute('''
                    INSERT INTO users 
                    (username, master_password, kdf_salt, encrypted_key)
                    VALUES (?, ?, ?, ?)
                ''', (username, hashed_password, kdf_salt, encrypted_key))

                Session.initialize(cur.lastrowid, username, encrypted_key)
                log_activity(t("Storage.Logging.Registration"))

            return True
        except sqlite3.IntegrityError:
            print(t("Storage.Register.UserExists"))
            return False

    @staticmethod
    def login(username: str, master_password: str) -> bool:
        try:
            row = conn.execute('''
                SELECT id, master_password, kdf_salt, encrypted_key 
                FROM users WHERE username = ?
            ''', (username,)).fetchone()

            if not row or not check_password(master_password, row[1]):
                return False

            user_id, _, kdf_salt, encrypted_key = row
            fernet_key = decrypt_user_key(master_password, kdf_salt, encrypted_key)

            Session.initialize(user_id, username, fernet_key)
            log_activity(t("Storage.Logging.Login"))
            return True

        except Exception as e:
            print(t("Storage.Login.FailedLogin"), {str(e)})
            return False

    @staticmethod
    def logout():
        log_activity(t("Storage.Logging.Logout"))
        Session.clear()

class PasswordManager:

    @staticmethod
    def check_password(password: str) -> bool:
        hashed_password = conn.execute("SELECT master_password FROM users WHERE id = ?", (Session.get_user_id(),)).fetchone()[0]
        return crypto.check_password(password, hashed_password)
    @staticmethod
    def save_password(service: str, password: str, note: str = ""):
        if not (key := Session.get_fernet_key()):
            raise ValueError(t("Storage.LoggedOut"))

        encrypted = encrypt_password(password, key)

        # Проверяем существующие записи
        existing = conn.execute('''
            SELECT service_name FROM passwords 
            WHERE user_id = ? AND service_name = ?
        ''', (Session.get_user_id(), service)).fetchall()

        if existing:
            print(t("Storage.SavePassword.ForService"), f"'{service}'", t("Storage.SavePassword.AlreadyExists") , len(existing), t("Storage.SavePassword.Passwords"))
            confirm = input(t("Storage.SavePassword.ConfirmSave"))
            if confirm.lower() not in ['y', 'да', 'yes']:
                return

        conn.execute('''
            INSERT INTO passwords (user_id, service_name, encrypted_password)
            VALUES (?, ?, ?)
        ''', (Session.get_user_id(), service, encrypted))
        conn.commit()
        log_activity(t("Storage.Logging.SavePassword"))

    @staticmethod
    def delete_password(pwd_id: int):
        conn.execute('''
            DELETE FROM passwords
            WHERE id = ? AND user_id = ?
        ''', (pwd_id, Session.get_user_id()))
        conn.commit()
        log_activity(f"Удаление пароля ID {pwd_id}")

    @staticmethod
    def update_password(pwd_id: int, new_password: str):
        encrypted = encrypt_password(new_password, Session.get_fernet_key())
        conn.execute('''
            UPDATE passwords
            SET encrypted_password = ?
            WHERE id = ? AND user_id = ?
        ''', (encrypted, pwd_id, Session.get_user_id()))
        conn.commit()
        log_activity(f"Обновление пароля ID {pwd_id}")

    @staticmethod
    def get_password(service: str) -> list:
        if not (key := Session.get_fernet_key()):
            raise ValueError(t("Storage.LoggedOut"))

        rows = conn.execute('''
            SELECT passwords.service_name, encrypted_password FROM passwords
            WHERE user_id = ? AND service_name = ?
        ''', (Session.get_user_id(), service)).fetchall()
        return [(row[0], decrypt_password(row[1], key)) for row in rows]

    @staticmethod
    def get_all_passwords() -> list:
        if not (key := Session.get_fernet_key()):
            raise ValueError(t("Storage.LoggedOut"))

        rows = conn.execute('''
            SELECT id, service_name, encrypted_password 
            FROM passwords
            WHERE user_id = ?
            ORDER BY created_at
        ''', (Session.get_user_id(),)).fetchall()

        return [
            (row[0], row[1], decrypt_password(row[2], key))
            for row in rows
        ]

def log_activity(action: str):
    if user_id := Session.get_user_id():
        conn.execute('''
            INSERT INTO activity_logs (user_id, action)
            VALUES (?, ?)
        ''', (user_id, action))
        conn.commit()
