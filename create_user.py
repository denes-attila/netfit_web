from database import get_db

conn = get_db()
cursor = conn.cursor()
cursor.execute(
    """
        INSERT INTO users (username, password) VALUES (?,?)
    """, ("attila", "password123")
)
conn.commit()
conn.close()
print("Felhasználó létrehozva!")