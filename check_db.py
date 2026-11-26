import sqlite3
from db import DB_PATH

conn = sqlite3.connect(DB_PATH)

print("Database:", DB_PATH)

print("\nConversations table:")
print(conn.execute(
    "PRAGMA table_info(conversations)"
).fetchall())

print("\nMessages table:")
print(conn.execute(
    "PRAGMA table_info(messages)"
).fetchall())

conn.close()