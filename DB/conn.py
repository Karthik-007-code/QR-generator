import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Database file location in the DB directory
DB_PATH = Path(__file__).resolve().parent / "users.db"


def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a SQLite connection with row factory enabled
    and multi-threading support for FastAPI.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes database tables if they do not already exist.
    """
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
    finally:
        conn.close()


def get_db():
    """
    FastAPI dependency and generator for database sessions.
    Automatically commits transactions on success and closes the connection.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


# Auto-initialize tables on module import
init_db()
