import sqlite3
from pathlib import Path
from i18n import t


def initialize_database():
    # Определяем абсолютный путь к базе данных
    db_path = Path(__file__).parent.parent / 'password_manager.db'

    # Создаем директорию если не существует
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA foreign_keys = ON")

        cursor = conn.cursor()

        # Проверяем существование таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.executescript('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    master_password TEXT NOT NULL,
                    kdf_salt TEXT NOT NULL,
                    encrypted_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    service_name TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );
            ''')

            # Создаем индексы
            cursor.execute('''
                CREATE INDEX idx_service_names 
                ON passwords(service_name)
            ''')

            conn.commit()
            print(t("InitDB.Created"))
        else:
            print(t("InitDB.AlreadyCreated"))

    except sqlite3.Error as e:
        print(t("InitDB.DatabaseError"), str(e))
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    initialize_database()