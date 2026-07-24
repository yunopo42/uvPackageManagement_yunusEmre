import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "database.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  #tuple yerine satır satır okumak amaçlı
    connection.execute("PRAGMA  foreign_keys = ON")
    return connection