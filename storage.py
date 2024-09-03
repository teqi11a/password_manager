import sqlite3
import bcrypt

# Подключение к базе данных
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

# Функция для создания нового пользователя
def create_user(username, master_password):
    hashed_password = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, master_password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Функция для авторизации пользователя
def authenticate_user(username, master_password):
    c.execute("SELECT master_password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(master_password.encode(), stored_password[0]):
        print("Авторизация успешна")
    else:
        print("Неправильное имя пользователя или пароль")

# Пример использования
create_user('user1', 'securepassword123')
authenticate_user('user1', 'securepassword123')
