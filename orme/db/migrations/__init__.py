import os
import sqlite3
from sqlite3 import Cursor, OperationalError
from typing import Tuple, List

from ...settings import DATABASE_URL, MIGRATIONS_PATH
from ..connection import create_connection_and_execute_query
from ..queries.queries_migrations import create, list_


# reasons
DB_DOES_NOT_EXIST = 'db-does-not-exist'
MIGRATIONS_NOT_RUNED = 'migrations-not-runed'


def create_migrations_table() -> None:
    create_connection_and_execute_query('create', create(), 'migrations')
    return


def app_need_migrations() -> Tuple[bool, Tuple[str]]:
    # if "create_migrations_table" is executed before this function,
    # it does not make sense to ask for the db creation since it will be created no
    # matter what
    if os.path.exists(DATABASE_URL):
        migration_files = os.listdir(MIGRATIONS_PATH)
        if migration_files:
            try:
                with sqlite3.connect(DATABASE_URL) as con:
                    cur: Cursor = con.cursor()

                    list_migrations_query: str = list_()[0]

                    cur.execute(list_migrations_query)
                    results: List[Tuple[str]] = cur.fetchall()

                    unnapplied_migrations = set(results) - set(migration_files)

                    if unnapplied_migrations:
                        return (True, (MIGRATIONS_NOT_RUNED,))

                    return (False,)
            except OperationalError as e:
                print(
                    f"The following error has ocurred when listing migrations: {e}")
    return False
