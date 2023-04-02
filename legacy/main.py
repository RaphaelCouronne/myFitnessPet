import sqlite3

if __name__ == "__main__":


    conn = sqlite3.connect('pet_database.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE pets (
        name TEXT PRIMARY KEY
    );''')

    conn.close()

