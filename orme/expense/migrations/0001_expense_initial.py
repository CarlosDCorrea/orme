import sqlite3
from ...settings import DATABASE_URL


def query_create() -> str:
    query: str = """
    CREATE TABLE if not exists expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        user TEXT,
        category TEXT NOT NULL,
        description TEXT,
        is_divided INTEGER NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
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
