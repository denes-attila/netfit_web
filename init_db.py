from database import get_db
import pandas as pd
from sqlalchemy import create_engine
import os

def load_csv(conn_string):
        engine = create_engine(conn_string)
        df = pd.read_csv("netfit.csv")
        df.to_sql("meresek", engine, if_exists="append", index=False)

def initialize_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
    )
    """
    )
    
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS meresek (
    id SERIAL PRIMARY KEY,
    nev TEXT,
    nem TEXT,
    kor INTEGER,
    sportolo TEXT,
    datum TEXT,
    suly INTEGER,
    magassag INTEGER,
    testzsir NUMERIC,
    tavolugrás INTEGER,
    ingafutas INTEGER,
    fekvotamasz INTEGER,
    hajlekonysag INTEGER,
    szoritoeró INTEGER,
    torzsemeles INTEGER
    )
    """
    )
    
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM meresek")
    count = cursor.fetchone()["count"]
    if count == 0:
        load_csv(os.getenv("DATABASE_URL"))
    conn.close()

if __name__ == "__main__":
    initialize_db()