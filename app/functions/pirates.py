def delete_pirate_by_id(pirate_id: str) -> bool:
    """Elimina un insulto por su id. Devuelve True si se eliminó, False si no existía."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM pirates WHERE id = ?", (pirate_id,))
        deleted = c.rowcount
        conn.commit()
        conn.close()
        return deleted > 0
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")


from app.schemas.pirates import PirateLangOut
import sqlite3
from typing import Optional
from app.schemas.pirates import Pirate, PirateCreate
from uuid import uuid4, UUID
import json

DB_PATH = "pirates.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS pirates (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        lang TEXT NOT NULL
    )"""
    )
    conn.commit()
    conn.close()


def add_pirate(pirate: PirateCreate) -> UUID:
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        pirate_id = str(uuid4())
        lang_dict = {pirate.lang: pirate.text}
        lang_json = json.dumps(lang_dict)
        c.execute(
            "INSERT INTO pirates (id, text, lang) VALUES (?, ?, ?)",
            (pirate_id, pirate.text, lang_json),
        )
        conn.commit()
        conn.close()
        return UUID(pirate_id)
    except Exception as e:
        # Aquí podrías loggear el error si quieres
        raise RuntimeError(f"Database error: {e}")


def get_pirates_by_lang_paginated(lang: str, page: int = 1, limit: int = 10):
    """
    Devuelve una tupla (items, total, page, limit, total_pages) de insultos filtrados por idioma y paginados.
    """
    try:
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
        filtered = [
            PirateLangOut(id=p.id, text=p.text, lang=p.lang)
            for p in pirates
            if p.lang == lang
        ]
        total = len(filtered)
        total_pages = (total + limit - 1) // limit if total > 0 else 1
        start = (page - 1) * limit
        end = start + limit
        items = filtered[start:end]
        return items, total, page, limit, total_pages
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")


def get_random_pirate() -> Optional[Pirate]:
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, text, lang FROM pirates ORDER BY RANDOM() LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row:
            lang_field = json.loads(row[2])
            if isinstance(lang_field, dict):
                lang_code, text = next(iter(lang_field.items()))
                return Pirate(id=UUID(row[0]), text=text, lang=lang_code)
            else:
                return Pirate(id=UUID(row[0]), text=row[1], lang=lang_field)
        return None
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
