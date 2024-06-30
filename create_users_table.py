import sqlite3

def init_user_db():
    conn = sqlite3.connect('hgwbanners.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
    conn.execute('''
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        ''', ('adminlephia', 'passwordlephia', 'admin',))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_user_db()
    print("User database and admin user created successfully")
