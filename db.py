import sqlite3

DB_NAME = "transactions.db"


# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        hour INTEGER,
        velocity REAL,
        new_user INTEGER,
        location TEXT,
        prediction INTEGER,
        score REAL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT TRANSACTION ----------------
def insert_transaction(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions 
    (amount, hour, velocity, new_user, location, prediction, score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# ---------------- GET ALL TRANSACTIONS ----------------
def get_all_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    conn.close()
    return rows