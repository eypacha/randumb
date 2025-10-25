
import sqlite3
from typing import Optional
from app.schemas.pirates import Pirate, PirateCreate
from uuid import uuid4, UUID
import json

DB_PATH = "pirates.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pirates (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        lang TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_pirate(pirate: PirateCreate) -> UUID:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pirate_id = str(uuid4())
    lang_dict = {pirate.lang: pirate.text}
    lang_json = json.dumps(lang_dict)
    c.execute("INSERT INTO pirates (id, text, lang) VALUES (?, ?, ?)", (pirate_id, pirate.text, lang_json))
    conn.commit()
    conn.close()
    return UUID(pirate_id)

def get_all_pirates() -> list[Pirate]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text, lang FROM pirates")
    rows = c.fetchall()
    conn.close()
    pirates = []
    for row in rows:
        lang_field = json.loads(row[2])
        if isinstance(lang_field, dict):
            lang_code, text = next(iter(lang_field.items()))
            pirates.append(Pirate(id=UUID(row[0]), text=text, lang=lang_code))
        else:
            pirates.append(Pirate(id=UUID(row[0]), text=row[1], lang=lang_field))
    return pirates

def get_random_pirate() -> Optional[Pirate]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text, lang FROM pirates ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return Pirate(id=UUID(row[0]), text=row[1], lang=json.loads(row[2]))
    return None
