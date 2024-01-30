import sqlite3
from argparse import Namespace

from ..settings import DATABASE_URL


def create_connection_and_execute_query(table_name: str, operation: str, args: Namespace):
    with sqlite3.connect(DATABASE_URL) as con:
        cur = con.cursor()

        # the cursor is going to be passed to the operation
        cur.close()
