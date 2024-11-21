import os
import sqlite3
import importlib

from datetime import date
from sqlite3 import Cursor, OperationalError
from typing import Tuple, List, Set, Dict

from ...settings import DATABASE_URL, MIGRATIONS_BASE_PATH, APPS
from ..connection import create_connection_and_execute_query
from ..queries.queries_migrations import create_table, insert_into, list_


def _create_migrations_table() -> None:
    create_connection_and_execute_query('create', create_table(), 'migrations')
    return


def _create_migration(*values: Dict[str, str | int]) -> None:
    data = {
        'model': 'debt',
        'name': '0001_initial_insert_into',
        'created': date.today().isoformat(),
    }

    print(insert_into(data)[1])

    create_connection_and_execute_query('create', insert_into(data), 'migrations')


def _get_unnaplied_migrations() -> Set[str]:
    # Iterate over all APPS/models and check for migrations
    # For each APP get the migrations's clean name to compare it with the registered migrations
    migrations = {app: {os.path.splitext(migration)[0]
                        for migration in os.listdir(os.path.join(MIGRATIONS_BASE_PATH, f"{app}/migrations"))
                        if os.path.isfile(migration)}
                  for app in APPS
                  }

    try:
        with sqlite3.connect(DATABASE_URL) as con:
            cur: Cursor = con.cursor()

            for app in APPS:
                list_migrations_query: str = list_(app)[0]

                cur.execute(list_migrations_query)
                results: List[Tuple[str]] = cur.fetchall()

                migrations[app] -= set([migration[2] for migration in results])
        return migrations
    except OperationalError as e:
        print(
            f"The following error has ocurred when cheking for unnaplied migrations: {e}")


def run_migrations() -> Tuple[bool, bool, Tuple[str]]:
    # There is always be a db because we need to have the migration table created
    _create_migrations_table()

    unnaplied_migrations: Dict[str] = _get_unnaplied_migrations()

    [print(f'({len(unnaplied_migrations[app])}) unnaplied migrations found for {app}')
     for app in unnaplied_migrations]

    if len(unnaplied_migrations.values()):
        for app, migrations in unnaplied_migrations.items():
            for migration in migrations:
                # We asume all users will have the migration dir
                print(migration)
                migration_to_run = importlib.import_module(
                    f'{migration}', '...expense.migrations')
                migration_to_run.run()
