"""SQLite connection and schema initialization."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator


DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "resumeiq.db"


@contextmanager
def get_connection(database_path: Path = DATABASE_PATH) -> Iterator[sqlite3.Connection]:
    """Open a SQLite connection with foreign-key support and safe transactions."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    """Create the local schema required by ResumeIQ's later phases."""
    with get_connection(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS role_skills (
                role_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                is_required INTEGER NOT NULL DEFAULT 1 CHECK (is_required IN (0, 1)),
                PRIMARY KEY (role_id, skill_id),
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
                FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                resume_name TEXT NOT NULL,
                ats_score INTEGER CHECK (ats_score BETWEEN 0 AND 100)
            );
            """
        )
