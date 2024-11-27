import sqlite3

from ...settings import DATABASE_URL


def query_create() -> str:
    query: str = """
    CREATE TABLE if not exists migrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        name TEXT,
        created TEXT,
        UNIQUE(model, name)
        );
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
