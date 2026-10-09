
import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "memories.db"


def get_connection():
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                created_at TEXT NOT NULL
            )
        """)
        connection.commit()
    finally:
        connection.close()


def save_memory(content, category="General"):
    if not isinstance(content, str) or not content.strip():
        return {"success": False, "message": "Memory cannot be empty."}

    content = content.strip()
    category = category.strip() if isinstance(category, str) else "General"
    category = category or "General"

    initialize_database()
    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT id FROM memories WHERE LOWER(content) = LOWER(?)",
            (content,)
        ).fetchone()

        if existing:
            return {
                "success": True,
                "message": "This memory is already saved.",
                "id": existing["id"]
            }

        created_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        cursor = connection.execute(
            """
            INSERT INTO memories (content, category, created_at)
            VALUES (?, ?, ?)
            """,
            (content, category, created_at)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Memory saved successfully.",
            "id": cursor.lastrowid
        }

    except sqlite3.Error as error:
        return {"success": False, "message": str(error)}

    finally:
        connection.close()


def get_all_memories():
    initialize_database()
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT id, content, category, created_at
            FROM memories
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def search_memories(query, limit=5):
    if not isinstance(query, str) or not query.strip():
        return []

    initialize_database()
    connection = get_connection()

    try:
        words = [
            word.strip(".,!?;:()[]{}\"'").lower()
            for word in query.split()
        ]
        words = list(dict.fromkeys(
            word for word in words if len(word) >= 2
        ))

        if not words:
            return []

        conditions = " OR ".join(
            ["LOWER(content) LIKE ?" for _ in words]
        )
        parameters = [f"%{word}%" for word in words]
        parameters.append(max(1, min(int(limit), 20)))

        rows = connection.execute(
            f"""
            SELECT id, content, category, created_at
            FROM memories
            WHERE {conditions}
            ORDER BY id DESC
            LIMIT ?
            """,
            parameters
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def delete_memory(memory_id):
    initialize_database()
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM memories WHERE id = ?",
            (int(memory_id),)
        )
        connection.commit()

        if cursor.rowcount:
            return {
                "success": True,
                "message": "Memory deleted successfully."
            }

        return {"success": False, "message": "Memory not found."}

    except (sqlite3.Error, ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    finally:
        connection.close()


def delete_all_memories():
    initialize_database()
    connection = get_connection()

    try:
        cursor = connection.execute("DELETE FROM memories")
        connection.commit()

        return {
            "success": True,
            "deleted_count": cursor.rowcount,
            "message": "All memories deleted successfully."
        }

    except sqlite3.Error as error:
        return {"success": False, "message": str(error)}

    finally:
        connection.close()


initialize_database()