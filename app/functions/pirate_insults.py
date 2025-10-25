import sqlite3
from typing import List, Optional
from app.schemas.pirate_insults import PirateInsult

DB_PATH = "pirate_insults.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pirate_insults (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_pirate_insult(insult: PirateInsult) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO pirate_insults (text) VALUES (?)", (insult.text,))
    conn.commit()
    insult_id = c.lastrowid
    conn.close()
    return insult_id

def get_random_pirate_insult() -> Optional[PirateInsult]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text FROM pirate_insults ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return PirateInsult(id=row[0], text=row[1])
    return None
