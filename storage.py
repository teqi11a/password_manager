import sqlite3
import bcrypt
import crypto




conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
session_id = 0
flag = False
user = ""

def create_user(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, master_password, salt) VALUES (?, ?, ?)", (username, hashed_password, crypto.generate_salt()))
    conn.commit()
    global user
    user = username
    log_activity(get_session_id(username), "Регистрация")
    user = ""

def authenticate_user(username, master_password):
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
