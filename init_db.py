import sqlite3

def initialize_db():
    conn = sqlite3.connect("netfit.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    """
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()