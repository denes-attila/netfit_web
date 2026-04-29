import psycopg2.extras  
import psycopg2
import os



def get_db():
    
    conn_string = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(conn_string, cursor_factory=psycopg2.extras.RealDictCursor)
    
    return conn