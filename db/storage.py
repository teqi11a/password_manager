import sqlite3
import bcrypt
from crypto import hash_password,check_password, encrypt_password, generate_key
from core.session import Session
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
session_id = 0
flag = False
user = ""
p = ""

class Helpers:


    @staticmethod
    def check_user(username, master_password):
        """
        Проверка существующего пользователя по мастер-паролю.
        """
        c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()
        if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
            return True
        else:
            print("Неправильное имя пользователя или пароль")

    @staticmethod
    def get_session_id(username):
        """
        Получение session_id пользователя.
        """
        try:
            __user_id = c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
            return __user_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_hashed_password():
        c.execute("SELECT master_password FROM users WHERE username = ?", (user,))
        return c.fetchone()[0]

    @staticmethod
    def load_key():
        c.execute("SELECT key FROM user_encryption_keys where user_id = ?", (session_id,))
        Session.set_user_key(c.fetchone()[0])
        return ''

class Auth:

    @staticmethod
    def authenticate_user(username, master_password):
        """
        Аутентификация пользователя с использованием хешированного пароля.
        """
        c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()[0]
        if check_password(master_password, stored_password):
            print("Авторизация успешна")
            global session_id, flag, user
            user = username
            session_id = Helpers.get_session_id(username)
            log_activity(session_id, "Авторизация")
            Helpers.load_key()
            flag = True
            return flag
        else:
            print("Неправильное имя пользователя или пароль")

    @staticmethod
    def logout() -> bool:
        """
        Выход из аккаунта.
        """
        global session_id, flag, user
        log_activity(Helpers.get_session_id(user), "Выход")
        session_id = 0
        flag = False
        user = ""
        print("Вы вышли из аккаунта")
        return flag

class UserActions:

    @staticmethod
    def create_user(username, master_password):
        """
        Создание пользователя с хешированным паролем и сохранением соли.
        """
        hashed_password, salt = hash_password(master_password)
        c.execute("INSERT INTO users (username, master_password, salt) VALUES (?, ?, ?)", (username, hashed_password.encode(), salt))
        conn.commit()

        global user
        user = username
        c.execute("INSERT INTO user_encryption_keys (user_id, key) VALUES (?, ?)", (Helpers.get_session_id(username), generate_key()))
        conn.commit()
        log_activity(Helpers.get_session_id(username), "Регистрация")
        user = ""


    @staticmethod
    def change_password(username, master_password):
        """
        Изменение мастер-пароля с обновлением хеша в базе данных. (В разработке)
        """
        c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()[0]
        if check_password(master_password, stored_password):
            hashed_password, salt = hash_password(master_password)
            c.execute("UPDATE users SET master_password = ?, salt = ? WHERE username = ?", (hashed_password, salt, username))
            conn.commit()
            log_activity(Helpers.get_session_id(username), "Смена пароля")


    @staticmethod
    def delete_user(username, master_password):
        """
        Удаление пользователя и всех его данных.
        """
        if not Helpers.check_user(username, master_password):
            print("Неправильное имя пользователя или пароль")
        else:
            user_id = Helpers.get_session_id(username)
            if user_id is not None:
                global user
                user = username
                c.execute("DELETE FROM users WHERE username = ?", (username,))
                c.execute("DELETE FROM passwords WHERE user_id = ?", (user_id,))
                log_activity(1, "Удаление аккаунта")
                user = ""
                conn.commit()
            else:
                print("User not found")



def save_passw(service, passw):
    passw = encrypt_password(passw)
    c.execute("INSERT INTO passwords (user_id, service, password) VALUES (?, ?, ?)",
              (session_id, service, passw))
    log_activity(Helpers.get_session_id(user), "Сохранение пароля")
    conn.commit()


def get_service(string: str):
    c.execute("SELECT service, password FROM passwords WHERE user_id = ? AND service = ?", (session_id, string))
    data = c.fetchall()
    log_activity(session_id, f'Получения пароля сервиса {string}')
    return data

def get_all_passwords():
    c.execute("SELECT service, password FROM passwords WHERE user_id = ?", (session_id,))
    data = c.fetchall()
    log_activity(session_id, f'Получение всех паролей')
    return data



def log_activity(user_id, action):
    """
    Логирование действий пользователя.
    """
    c.execute("INSERT INTO activity_logs (user_id, action, username) VALUES (?, ?, ?)", (user_id, action, user))
    conn.commit()