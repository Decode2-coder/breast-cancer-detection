import sqlite3
from datetime import datetime

DB_PATH = None  # Set by run.py

def init_db(path):
    global DB_PATH
    DB_PATH = path
    print(f"📦 Using DB at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            prediction TEXT,
            confidence REAL,
            wallet_address TEXT,
            image_type TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_history(filename, prediction, confidence, wallet_address, image_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (timestamp, filename, prediction, confidence, wallet_address, image_type) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), filename, prediction, confidence, wallet_address, image_type)
    )
    conn.commit()
    conn.close()

def fetch_history(wallet_address):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, filename, prediction, confidence, image_type
        FROM history
        WHERE wallet_address = ?
        ORDER BY id DESC
    """, (wallet_address,))
    rows = c.fetchall()
    conn.close()
    return rows
