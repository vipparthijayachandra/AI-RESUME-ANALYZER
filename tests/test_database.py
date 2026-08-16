"""Tests for Phase 2 SQLite foundation setup."""

import sqlite3
from pathlib import Path

from app.data.database import get_connection, initialize_database


def test_initialize_database_creates_expected_schema(tmp_path: Path) -> None:
    """The initializer creates all planned foundation tables."""
    database_path = tmp_path / "nested" / "resumeiq.db"

    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert {"roles", "skills", "role_skills", "analysis_history"} <= tables


def test_connection_commits_successful_transactions(tmp_path: Path) -> None:
    """Successful work is committed when the connection context exits."""
    database_path = tmp_path / "resumeiq.db"
    initialize_database(database_path)

    with get_connection(database_path) as connection:
        connection.execute(
            "INSERT INTO roles (name, description) VALUES (?, ?)",
            ("Data Analyst", "Works with data to produce insights."),
        )

    with sqlite3.connect(database_path) as connection:
        stored_role = connection.execute("SELECT name FROM roles").fetchone()

    assert stored_role == ("Data Analyst",)


def test_connection_rolls_back_failed_transactions(tmp_path: Path) -> None:
    """Failed work is not persisted to the local database."""
    database_path = tmp_path / "resumeiq.db"
    initialize_database(database_path)

    try:
        with get_connection(database_path) as connection:
            connection.execute(
                "INSERT INTO roles (name, description) VALUES (?, ?)",
                ("Software Engineer", "Builds software products."),
            )
            raise RuntimeError("Simulated failure")
    except RuntimeError:
        pass

    with sqlite3.connect(database_path) as connection:
        role_count = connection.execute("SELECT COUNT(*) FROM roles").fetchone()[0]

    assert role_count == 0
