import sqlite3

conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    master_password TEXT NOT NULL
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
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
