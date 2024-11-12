import sqlite3
from typing import List, Tuple

from orme.db.operations import create, list_, update, delete, total, get
from orme.settings import DATABASE_URL


def create_connection_and_execute_query(operation: str,
                                        queries: List[str],
                                        table_name: str) -> Tuple[str | int] | None:
    with sqlite3.connect(DATABASE_URL) as con:
        cur = con.cursor()

        if operation == 'create':
            create(cur, con, queries, table_name)

        if operation == 'list':
            list_(cur, queries, table_name)

        if operation == 'update':
            update(cur, con, queries)

        if operation == 'delete':
            delete(cur, con, queries)

        if operation == 'total':
            total(cur, queries)

        if operation == 'get':
            return get(cur, queries)

    print('connection closed')
