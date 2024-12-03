import sqlite3
from ...settings import DATABASE_URL


def query_create() -> str:
    query: str = """
    CREATE TABLE if not exists users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name INTEGER NOT NULL,
        last_name TEXT NOT NULL,
        created TEXT,
        updated TEXT)
    """

    return query


def run() -> None:
    # Query Execution
    try:
        with sqlite3.connect(DATABASE_URL) as con:
            cur: sqlite3.Cursor = con.cursor()

            cur.execute(query_create())
            con.commit()
    except sqlite3.OperationalError as e:
        print(f'An error ocurred while executing migration {e}')
