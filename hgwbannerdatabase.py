import sqlite3

def init_db():
    conn = sqlite3.connect('hgwbanners.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS hgwbanners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Game_title TEXT NOT NULL,
            Banner_type TEXT NOT NULL,
            Name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
            
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database and table created successfully")