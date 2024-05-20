import sqlite3
from typing import List

from orme.db.operations import create, list_, update, delete
from orme.settings import DATABASE_URL


def create_connection_and_execute_query(operation: str, queries: List[str], table_name: str):
    with sqlite3.connect(DATABASE_URL) as con:
        cur = con.cursor()

        if operation == 'create':
            create(cur, con, queries, table_name)

        if operation == 'list':
            list_(cur, con, queries, table_name)

        if operation == 'update':
            update(cur, con, queries, table_name)

        if operation == 'delete':
            delete(cur, con, queries, table_name)

    print('connection closed')
