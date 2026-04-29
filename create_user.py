from database import get_db
from werkzeug.security import generate_password_hash

conn = get_db()
cursor = conn.cursor()

cursor.execute(
    """
        INSERT INTO users (username, password) VALUES (%s,%s)
    """, ("attila", generate_password_hash("password123"))
)
conn.commit()
conn.close()
print("Felhasználó létrehozva!")