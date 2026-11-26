
import sqlite3
import uuid
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "studymate.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS feature_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                feature_name TEXT NOT NULL,
                input_data TEXT NOT NULL,
                output_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_progress (
                conversation_id TEXT PRIMARY KEY,
                quiz_data TEXT NOT NULL,
                answers TEXT NOT NULL,
                current_index INTEGER NOT NULL DEFAULT 0,
                is_submitted INTEGER NOT NULL DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)


def create_conversation(title="New Chat"):

    init_db()

    conversation_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO conversations (id, title)
            VALUES (?, ?)
        """, (conversation_id, title))

    return conversation_id


def get_conversations():

    init_db()

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, created_at
            FROM conversations
            ORDER BY created_at DESC, rowid DESC
        """).fetchall()

    return [dict(row) for row in rows]


def get_messages(conversation_id):

    init_db()

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (conversation_id,)).fetchall()

    return [dict(row) for row in rows]


def save_message(conversation_id, role, content):

    init_db()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, role, content))


def update_conversation_title(conversation_id, title):

    init_db()

    with get_connection() as conn:
        conn.execute("""
            UPDATE conversations
            SET title = ?
            WHERE id = ?
        """, (title[:50], conversation_id))


def delete_conversation(conversation_id):

    init_db()

    with get_connection() as conn:
        conn.execute("""
            DELETE FROM conversations
            WHERE id = ?
        """, (conversation_id,))


def save_feature_history(
    conversation_id,
    feature_name,
    input_data,
    output_data
):
    init_db()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO feature_history (
                conversation_id,
                feature_name,
                input_data,
                output_data
            )
            VALUES (?, ?, ?, ?)
        """, (
            conversation_id,
            feature_name,
            json.dumps(input_data, ensure_ascii=False),
            output_data
        ))


def get_feature_history(conversation_id, feature_name=None):
    init_db()

    with get_connection() as conn:

        if feature_name:
            rows = conn.execute("""
                SELECT id, feature_name, input_data,
                       output_data, created_at
                FROM feature_history
                WHERE conversation_id = ?
                AND feature_name = ?
                ORDER BY id DESC
            """, (conversation_id, feature_name)).fetchall()

        else:
            rows = conn.execute("""
                SELECT id, feature_name, input_data,
                       output_data, created_at
                FROM feature_history
                WHERE conversation_id = ?
                ORDER BY id DESC
            """, (conversation_id,)).fetchall()

    history = []

    for row in rows:
        item = dict(row)
        item["input_data"] = json.loads(item["input_data"])
        history.append(item)

    return history


def save_quiz_progress(
    conversation_id,
    quiz_data,
    answers,
    current_index,
    is_submitted
):
    import json

    init_db()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO quiz_progress (
                conversation_id,
                quiz_data,
                answers,
                current_index,
                is_submitted,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(conversation_id)
            DO UPDATE SET
                quiz_data = excluded.quiz_data,
                answers = excluded.answers,
                current_index = excluded.current_index,
                is_submitted = excluded.is_submitted,
                updated_at = CURRENT_TIMESTAMP
        """, (
            conversation_id,
            json.dumps(quiz_data, ensure_ascii=False),
            json.dumps(answers, ensure_ascii=False),
            current_index,
            int(is_submitted)
        ))


def get_quiz_progress(conversation_id):
    import json

    init_db()

    with get_connection() as conn:
        row = conn.execute("""
            SELECT quiz_data, answers, current_index, is_submitted
            FROM quiz_progress
            WHERE conversation_id = ?
        """, (conversation_id,)).fetchone()

    if row is None:
        return None

    return {
        "quiz_data": json.loads(row["quiz_data"]),
        "answers": {
            int(key): value
            for key, value in json.loads(row["answers"]).items()
        },
        "current_index": row["current_index"],
        "is_submitted": bool(row["is_submitted"])
    }


def delete_quiz_progress(conversation_id):
    init_db()

    with get_connection() as conn:
        conn.execute("""
            DELETE FROM quiz_progress
            WHERE conversation_id = ?
        """, (conversation_id,))