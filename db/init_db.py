import sqlite3
import os

db_path = os.path.abspath('../password_manager.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    master_password TEXT NOT NULL,
    salt BLOB NOT NULL
)
''')

c.execute('''
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    password TEXT NOT NULL,
    service TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

c.execute('''
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL DEFAULT 'unknown',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
