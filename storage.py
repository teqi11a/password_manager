import sqlite3
import bcrypt


conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
session_id = 0
flag = False


def get_session_id(username):
    try:
        __user_id = c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        return __user_id
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_user(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, master_password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

def authenticate_user(username, master_password):
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        print("Авторизация успешна")
        global session_id, flag
        session_id = get_session_id(username)
        log_activity(1, "Авторизация")
        flag = True
        return flag
    else:
        print("Неправильное имя пользователя или пароль")

def check_user(username, master_password):
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        return True
    else:
        print("Неправильное имя пользователя или пароль")



def change_password(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("UPDATE users SET master_password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    log_activity(1, "Смена пароля")


def log_activity(user_id, action):
    c.execute("INSERT INTO activity_logs (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()

def save_passw(passw, service):
    c.execute("INSERT INTO passwords (user_id, password, service) VALUES (?, ?, ?)", (session_id, service, passw))
    conn.commit()

def unlogin() -> bool:
    global session_id, flag
    session_id = 0
    flag = False
    return flag
