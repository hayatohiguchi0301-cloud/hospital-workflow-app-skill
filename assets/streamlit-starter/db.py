from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "app.db"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize(db_path: Path | None = None) -> None:
    conn = connect(db_path)
    try:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(trim(title)) > 0),
                owner TEXT NOT NULL DEFAULT '', due_date TEXT,
                status TEXT NOT NULL DEFAULT '未着手', note TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.commit()
    finally:
        conn.close()


def list_tasks(query: str = "", status: str = "") -> list[sqlite3.Row]:
    sql = "SELECT * FROM tasks WHERE (title LIKE ? OR owner LIKE ? OR note LIKE ?)"
    term = f"%{query.strip()}%"
    params: list[object] = [term, term, term]
    if status:
        sql += " AND status = ?"
        params.append(status)
    sql += " ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date, id DESC"
    conn = connect()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def create_task(title: str, owner: str, due_date: str | None, status: str, note: str) -> int:
    title = title.strip()
    if not title:
        raise ValueError("件名を入力してください。")
    conn = connect()
    try:
        cursor = conn.execute("INSERT INTO tasks(title, owner, due_date, status, note) VALUES (?, ?, ?, ?, ?)", (title, owner.strip(), due_date or None, status, note.strip()))
        conn.commit()
        return int(cursor.lastrowid)
    finally:
        conn.close()


def update_task(task_id: int, title: str, owner: str, due_date: str | None, status: str, note: str) -> None:
    title = title.strip()
    if not title:
        raise ValueError("件名を入力してください。")
    conn = connect()
    try:
        conn.execute("UPDATE tasks SET title=?, owner=?, due_date=?, status=?, note=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (title, owner.strip(), due_date or None, status, note.strip(), task_id))
        conn.commit()
    finally:
        conn.close()


def delete_task(task_id: int) -> None:
    conn = connect()
    try:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    finally:
        conn.close()