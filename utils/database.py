import sqlite3

def setup_database():
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS highscores
                      (user_id INTEGER, user_name TEXT, chat_id INTEGER, score INTEGER,
                       PRIMARY KEY (user_id, chat_id))''')

    conn.commit()
    conn.close()
    
def setup_databasee():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER, chat_id INTEGER,
                       PRIMARY KEY (user_id, chat_id))''')

    conn.commit()
    conn.close()
