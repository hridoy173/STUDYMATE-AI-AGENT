
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "studymate.db"

if DB_PATH.exists():
    DB_PATH.unlink()
    print("Old database deleted successfully!")
else:
    print("Database does not exist.")

print("Database is ready to be recreated.")
