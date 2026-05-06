import sqlite3
from typing import List

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# CREATE TABLE (SAFE INIT)
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# -----------------------------
# SAVE MESSAGE
# -----------------------------
def save_message(user_id: str, message: str) -> None:
    cursor.execute(
        "INSERT INTO memory (user_id, message) VALUES (?, ?)",
        (user_id, message)
    )
    conn.commit()


# -----------------------------
# GET LAST MESSAGES (LIMITED + ORDERED)
# -----------------------------
def get_memory(user_id: str, limit: int = 10) -> List[str]:
    cursor.execute(
        """
        SELECT message 
        FROM memory 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cursor.fetchall()

    # reverse to maintain conversation order (old → new)
    return [row[0] for row in reversed(rows)]


# -----------------------------
# CLEAR USER MEMORY (OPTIONAL TOOL)
# -----------------------------
def clear_memory(user_id: str) -> None:
    cursor.execute(
        "DELETE FROM memory WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()