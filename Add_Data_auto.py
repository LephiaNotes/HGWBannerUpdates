import sqlite3

def add_banner(game_title, banner_type, name, start_date, end_date):
    conn = sqlite3.connect('hgwbanners.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO hgwbanners (Game_title, banner_type, Name, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (game_title, banner_type, name, start_date, end_date))
    conn.commit()
    conn.close()

def get_banner_details():
    game_title = input("Enter Game Title: ")
    banner_type = input("Character or Weapon type?: ")
    name = input("Character or weapon name: ")
    start_date = input("Starting Date: ")
    end_date = input("End date: ")
    return (game_title, banner_type, name, start_date, end_date)

if __name__ == '__main__':
    while True:
        banner_details = get_banner_details()
        add_banner(*banner_details)
        print("Banner added successfully")
        next_banner = input("Do you want to add another banner? (yes/no): ").strip().lower()
        if next_banner != 'yes':
            break