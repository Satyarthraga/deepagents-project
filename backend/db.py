import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "runs.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                prd_summary TEXT,
                service TEXT,
                branch TEXT,
                status TEXT DEFAULT 'running',
                pr_url TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                type TEXT,
                content TEXT,
                created_at TEXT
            );
        """)


def create_run(run_id: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO runs (id, status, created_at) VALUES (?, 'running', ?)",
            (run_id, datetime.utcnow().isoformat()),
        )


def update_run(run_id: str, **kwargs):
    if not kwargs:
        return
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    with get_conn() as conn:
        conn.execute(f"UPDATE runs SET {sets} WHERE id = ?", (*kwargs.values(), run_id))


def save_event(run_id: str, type_: str, content):
    payload = content if isinstance(content, str) else json.dumps(content)
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO events (run_id, type, content, created_at) VALUES (?, ?, ?, ?)",
            (run_id, type_, payload, datetime.utcnow().isoformat()),
        )


def get_runs():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM runs ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
        return [dict(r) for r in rows]


def get_events(run_id: str):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE run_id = ? ORDER BY id ASC", (run_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_run(run_id: str):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return dict(row) if row else None
