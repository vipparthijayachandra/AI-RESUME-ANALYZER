"""Small data-access helpers for role and skill information."""

from app.data.database import get_connection
from app.models.schemas import JobRole


def list_roles() -> list[JobRole]:
    """Return all configured job roles in name order."""
    with get_connection() as connection:
        rows = connection.execute("SELECT name, description FROM roles ORDER BY name").fetchall()
    return [JobRole(name=row[0], description=row[1]) for row in rows]
