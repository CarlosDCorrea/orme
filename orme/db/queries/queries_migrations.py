from datetime import date
from typing import Tuple


TABLE_NAME = 'migrations'


def create() -> Tuple[str]:
    create_query = f"""
    CREATE TABLE if not exists {TABLE_NAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        name TEXT,
        created TEXT,
        UNIQUE(model, name)
        );
    """

    return (create_query,)


def insert_into(*values: Tuple[str]) -> Tuple[str]:
    model: str = values[0]
    name: str = values[1]
    today = date.today().isoformat()

    insert_into: str = f"""
    INSERT INTO {TABLE_NAME}(
        name,
        state,
        created,
        updated) VALUES(
            '{model}',
            '{name}',
            '{today}',
            );"""

    return (insert_into,)


def list_() -> Tuple[str]:
    list_query: str = f"""
    SELECT * FROM {TABLE_NAME};
    """

    return (list_query,)
