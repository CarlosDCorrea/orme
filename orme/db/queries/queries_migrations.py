from typing import Tuple


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


def list_(model: str) -> Tuple[str]:
    list_query: str = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE model = '{model}';
    """

    return (list_query,)
