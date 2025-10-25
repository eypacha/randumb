
import sqlite3
from typing import List, Optional
from app.schemas.pirates import Pirate

DB_PATH = "pirates.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pirates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_pirate(pirate: Pirate) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO pirates (text) VALUES (?)", (pirate.text,))
    conn.commit()
    pirate_id = c.lastrowid
    conn.close()
    return pirate_id

def get_all_pirates() -> list[Pirate]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text FROM pirates")
    rows = c.fetchall()
    conn.close()
    return [Pirate(id=row[0], text=row[1]) for row in rows]
import sqlite3
from typing import List, Optional
from app.schemas.pirates import Pirate

DB_PATH = "pirates.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pirates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_pirate(pirate: Pirate) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO pirates (text) VALUES (?)", (pirate.text,))
    conn.commit()
    pirate_id = c.lastrowid
    conn.close()
    return pirate_id

