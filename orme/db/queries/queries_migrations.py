from typing import Tuple, Dict


TABLE_NAME = 'migrations'


# All creations should be in migrations files
def create_table() -> Tuple[str]:
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


def insert_into(data: Dict[str, Tuple[str | int]]) -> Tuple[str]:
    character = ', \n'
    insert_into: str = f"""
    INSERT INTO {TABLE_NAME}(
        {character.join(data)}) VALUES(
        {character.join([f"'{value}'"
                         if isinstance(value, str)
                         else value
                         for value in data.values()])}
            );"""

    return ('', insert_into)


def list_(model: str) -> Tuple[str]:
    list_query: str = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE model = '{model}';
    """

    return (list_query,)
