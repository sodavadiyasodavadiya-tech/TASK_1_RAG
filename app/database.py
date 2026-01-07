import sqlite3

DB_NAME = "rag.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document TEXT,
        chunk_id INTEGER,
        text TEXT,
        embedding BLOB
    )
    """)

    conn.commit()
    conn.close()
