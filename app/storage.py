# storage.py
import json
from pathlib import Path

DB_FILE = Path("contest_users.json")

def save_user(number, data):
    users = load_users()
    users[number] = data
    DB_FILE.write_text(json.dumps(users, indent=2))

def load_users():
    if not DB_FILE.exists():
        return {}
    return json.loads(DB_FILE.read_text())
