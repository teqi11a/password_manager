import sqlite3
import bcrypt
import crypto

conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
session_id = 0
flag = False
user = ""
p = ""


def create_user(username, master_password):
    """
    Создание пользователя с хешированным паролем и сохранением соли.
    """
    salt = crypto.generate_salt()  # Генерируем соль
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, master_password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
    conn.commit()
    global user
    user = username
    log_activity(get_session_id(username), "Регистрация")
    user = ""


def authenticate_user(username, master_password):
    """
    Аутентификация пользователя с использованием хешированного пароля.
    """
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        print("Авторизация успешна")
        global session_id, flag, user
        user = username
        session_id = get_session_id(username)
        log_activity(session_id, "Авторизация")
        flag = True
        return flag
    else:
        print("Неправильное имя пользователя или пароль")


def log_activity(user_id, action):
    """
    Логирование действий пользователя.
    """
    c.execute("INSERT INTO activity_logs (user_id, action, username) VALUES (?, ?, ?)", (user_id, action, user))
    conn.commit()


def change_password(username, master_password):
    """
    Изменение мастер-пароля с обновлением хеша в базе данных.
    """
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("UPDATE users SET master_password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    log_activity(get_session_id(username), "Смена пароля")


def save_passw(service, passw):
    c.execute("INSERT INTO passwords (user_id, service, password) VALUES (?, ?, ?)",
              (session_id, service, passw))
    log_activity(get_session_id(user), "Сохранение пароля")
    conn.commit()



def delete_user(username, master_password):
    """
    Удаление пользователя и всех его данных.
    """
    if not check_user(username, master_password):
        print("Неправильное имя пользователя или пароль")
    else:
        user_id = get_session_id(username)
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


def logout() -> bool:
    """
    Выход из аккаунта.
    """
    global session_id, flag, user
    log_activity(get_session_id(user), "Выход")
    session_id = 0
    flag = False
    user = ""
    print("Вы вышли из аккаунта")
    return flag
