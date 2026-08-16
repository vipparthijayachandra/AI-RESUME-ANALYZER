"""Seed-data entry point reserved for the role catalog phase."""

from app.data.database import initialize_database


def seed_database() -> None:
    """Ensure the database schema exists; curated roles are added in Phase 1 data design."""
    initialize_database()
