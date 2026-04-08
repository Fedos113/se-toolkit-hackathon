"""
Event Countdown Timer - Database Module
Handles SQLite database initialization and operations.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

# Use /app/data in Docker, fallback to local dir
DATA_DIR = os.getenv('DATA_DIR', os.path.join(os.path.dirname(__file__), 'data'))
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE_PATH = os.path.join(DATA_DIR, "events.db")


def get_db_connection() -> sqlite3.Connection:
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the events table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            target_datetime TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            user_session_id TEXT,
            notified BOOLEAN DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()


def create_event(title: str, target_datetime: str, user_session_id: Optional[str] = None) -> Dict:
    """Create a new event in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO events (title, target_datetime, created_at, user_session_id, notified) VALUES (?, ?, ?, ?, 0)",
        (title, target_datetime, datetime.utcnow().isoformat(), user_session_id)
    )
    
    event_id = cursor.lastrowid
    conn.commit()
    
    # Fetch the created event
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = dict(cursor.fetchone())
    
    conn.close()
    return event


def get_events_by_session_id(user_session_id: str) -> List[Dict]:
    """Retrieve all events for a specific user session."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE user_session_id = ? ORDER BY target_datetime ASC",
        (user_session_id,)
    )
    events = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return events


def get_unnotified_past_events_by_session_id(user_session_id: str) -> List[Dict]:
    """Get events for a specific user that have passed but haven't been notified yet."""
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    cursor.execute(
        "SELECT * FROM events WHERE target_datetime <= ? AND notified = 0 AND user_session_id = ? ORDER BY target_datetime ASC",
        (now, user_session_id)
    )
    events = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return events


def get_event_by_id(event_id: int) -> Optional[Dict]:
    """Retrieve a single event by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    
    conn.close()
    return dict(row) if row else None


def delete_event(event_id: int) -> bool:
    """Delete an event by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()

    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_event_by_session_id(event_id: int, user_session_id: str) -> bool:
    """Delete an event by ID only if it belongs to the specified user session."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM events WHERE id = ? AND (user_session_id = ? OR user_session_id IS NULL)",
        (event_id, user_session_id)
    )
    conn.commit()

    affected = cursor.rowcount
    conn.close()
    return affected > 0


def update_event_notified(event_id: int) -> bool:
    """Mark an event as notified."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE events SET notified = 1 WHERE id = ?", (event_id,))
    conn.commit()
    
    affected = cursor.rowcount
    conn.close()
    return affected > 0


# Initialize database on module import
init_db()
