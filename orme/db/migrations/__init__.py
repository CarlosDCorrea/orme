import os
import sqlite3
import importlib
from datetime import date

from sqlite3 import Cursor, OperationalError
from typing import Tuple, List, Set, Dict

from ...settings import DATABASE_URL, MIGRATIONS_BASE_PATH, APPS
from ..connection import create_connection_and_execute_query
from ..queries.queries_migrations import list_
from ...db.queries.common_queries import generate_insert_into_query


def _create_migration_table() -> None:
    query: str = """
    CREATE TABLE if not exists migrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT,
        name TEXT,
        created TEXT,
        UNIQUE(app, name)
        );
    """

    try:
        with sqlite3.connect(DATABASE_URL) as con:
            cur: sqlite3.Cursor = con.cursor()

            cur.execute(query)
            con.commit()
    except sqlite3.OperationalError as e:
        print(f'An error ocurred while executing migration {e}')


def _create_migration(data: Dict[str, str | int]) -> None:
    create_connection_and_execute_query(
        'create', generate_insert_into_query(data, 'migrations'), 'migrations')
    return


def _get_unnaplied_migrations() -> Set[str]:
    # Iterate over all APPS/models and check for migrations
    # For each APP get the migrations's clean name to compare it with the registered migrations
    migrations = {app: {os.path.splitext(migration)[0]
                        for migration in os.listdir(os.path.join(MIGRATIONS_BASE_PATH, f"{app}/migrations"))
                        if os.path.isfile(os.path.join(MIGRATIONS_BASE_PATH, f'{app}/migrations/{migration}'))}
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
    _create_migration_table()
    unnaplied_migrations: Dict[str, Set[str]] = _get_unnaplied_migrations()

    """ [print(f'({len(unnaplied_migrations[app])}) unnaplied migrations found for {app}')
     for app in unnaplied_migrations] """

    # Make sure at least one of the migrations sets inside the dictionary have unnaplied migrations
    if [migrations_set for migrations_set in unnaplied_migrations.values() if len(migrations_set)]:
        print(f"Migrations to be applied found for apps {', '.join(unnaplied_migrations)}")

        for app, migrations in unnaplied_migrations.items():
            for migration in migrations:
                # We asume all users will have the migration dir
                migration_to_run = importlib.import_module(
                    f'.{migration}', f'orme.{app}.migrations')
                migration_to_run.run()

                print(f'- {migration} applied for app {app}')

                # Add the migration to the migrations table after it was successfully runed
                data: Dict[str, Tuple[str | int]] = {
                    'app': f'{app}',
                    'name': f'{migration}',
                    'created': date.today().isoformat()
                }

                _create_migration(data)
