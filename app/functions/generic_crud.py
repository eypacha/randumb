import sqlite3
from uuid import uuid4, UUID
import json
from typing import List
from pydantic import BaseModel
import random

DB_PATH = "dumb.db"


def create_item(resource: str, item: BaseModel):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        item_id = str(uuid4())
        lang_dict = {item.lang: item.text}
        lang_json = json.dumps(lang_dict)
        c.execute(
            f"INSERT INTO {resource} (id, text, lang) VALUES (?, ?, ?)",
            (item_id, item.text, lang_json),
        )
        conn.commit()
        conn.close()
        return {"id": item_id, "text": item.text, "lang": item.lang}
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")


def list_items_by_lang(resource: str, lang: str, page: int, limit: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"SELECT id, text, lang FROM {resource}")
        rows = c.fetchall()
        conn.close()
        items = []
        for row in rows:
            lang_field = json.loads(row[2])
            if isinstance(lang_field, dict):
                lang_code, text = next(iter(lang_field.items()))
                if lang_code == lang:
                    items.append({"id": row[0], "text": text, "lang": lang_code})
            else:
                if lang_field == lang:
                    items.append({"id": row[0], "text": row[1], "lang": lang_field})
        total = len(items)
        total_pages = (total + limit - 1) // limit if total > 0 else 1
        start = (page - 1) * limit
        end = start + limit
        paginated = items[start:end]
        return {
            "items": paginated,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
        }
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")


def init_tables(resources: dict):
    """Inicializa las tablas para cada recurso si no existen."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for resource, config in resources.items():
            table = config["table"]
            c.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    lang TEXT NOT NULL
                )
            """
            )
        conn.commit()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Database initialization error: {e}")


def get_random_item(resource: str, lang: str = None):
    """Return a random item from the given resource.

    If `lang` is provided, only items matching that language will be considered.
    Returns a dict with keys 'id', 'text', 'lang' or None if no matching items.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"SELECT id, text, lang FROM {resource}")
        rows = c.fetchall()
        conn.close()

        candidates = []
        for row in rows:
            # row: (id, text, lang)
            lang_field = json.loads(row[2])
            if isinstance(lang_field, dict):
                lang_code, text_val = next(iter(lang_field.items()))
            else:
                lang_code = lang_field
                text_val = row[1]

            if lang is None or lang_code == lang:
                candidates.append({"id": row[0], "text": text_val, "lang": lang_code})

        if not candidates:
            return None

        return random.choice(candidates)
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
