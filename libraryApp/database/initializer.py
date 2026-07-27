from pathlib import Path

from database.connections import get_connection

SCHEMA_PATH = Path(__file__).resolve().parent /"schema.sql"

def initialize_database():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = get_connection()
    try:
        connection.executescript(schema)
        connection.commit()
    finally:
        connection.close()