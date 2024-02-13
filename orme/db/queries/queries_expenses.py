from argparse import Namespace
import sqlite3
from sqlite3 import Cursor, Connection
from datetime import date
from typing import Union, List, Tuple

from pandas import DataFrame

from ...validations import validate_date


TABLE_NAME = 'expenses'
get_table_columns_query = f'PRAGMA table_info({TABLE_NAME})'


def create(cur: Cursor, con: Connection, args: Namespace):
    validate_date(args.date)
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

    cur = con.cursor()

    create_expenses_table_query = """
    CREATE TABLE if not exists expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        user TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        is_divided INTEGER NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
    """

    insert_into_expenses_query = f"""
    INSERT INTO expenses(
        value,
        user,
        category,
        description,
        is_divided,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.user}',
            '{args.category}',
            '{args.description}',
            {is_divided},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    cur.execute(create_expenses_table_query)
    cur.execute(insert_into_expenses_query)
    con.commit()
    cur.close()

    print('The expense was registered successfully...')


def list_(cur: Cursor, con: Connection):
    offset = 0
    limit = 10

    query_results = f"""
            SELECT *
            FROM expenses
            ORDER BY date DESC
            LIMIT {offset}, {limit}
            """

    query_count = """
            SELECT COUNT(*)
            FROM expenses
            """

    try:
        cur.execute(get_table_columns_query)
        columns: List[Tuple[Union[int, str]]] = cur.fetchall()

        # TODO: use pandas sql reader instead of cur to retrieve the rows
        # get the requested data
        cur.execute(query_results)
        results: List[Tuple[Union[str, int]]] = cur.fetchall()

        # get the count of the table's rows
        cur.execute(query_count)
        count: int = cur.fetchone()[0]

        print('number of register for this query:: ', count)

        data = DataFrame.from_records(data=results,
                                      columns=[column[1] for column in columns])

        if data.empty:
            print('Nothing to show')
            return

        print(data)

    except sqlite3.OperationalError as e:
        error = f'We can\'t perform this action because the table {TABLE_NAME} does not exists'
        print('This is the real error')
        print(e)
        print(f'error {error}')
        cur.close()


def list_by_date(cur: Cursor, con: Connection, where_statement: str):
    offset = 0
    limit = 10

    query_results = f"""
            SELECT *
            FROM {TABLE_NAME}
            WHERE date {where_statement}
            ORDER BY date DESC
            LIMIT {offset}, {limit}
            """

    query_count = f"""
            SELECT COUNT(*)
            FROM {TABLE_NAME}
            WHERE date {where_statement}
            """

    try:
        cur.execute(get_table_columns_query)
        columns: List[Tuple[Union[int, str]]] = cur.fetchall()

        cur.execute(query_results)
        results: List[Tuple[Union[str, int]]] = cur.fetchall()

        cur.execute(query_count)
        count: int = cur.fetchone()[0]

        print('number of register for this query:: ', count)

        data = DataFrame.from_records(data=results,
                                      columns=[column[1] for column in columns])

        if data.empty:
            print('Nothing to show')
            return

        print(data)

    except sqlite3.OperationalError as e:
        error = f'We can\'t perform this action because the table {TABLE_NAME} does not exists'
        print('This is the real error')
        print(e)
        print(f'error {error}')
        cur.close()


def list_by_value(cur: Cursor, con: Connection, where_statement: str):
    offset = 0
    limit = 10

    query_results = f"""
        SELECT *
        FROM '{TABLE_NAME}'
        WHERE value {where_statement}
        ORDER BY date DESC
        LIMIT {offset}, {limit}
        """

    query_count = f"""
            SELECT COUNT(*)
            FROM '{TABLE_NAME}'
            WHERE value {where_statement}
            """

    try:
        cur.execute(get_table_columns_query)
        columns: List[Tuple[Union[int, str]]] = cur.fetchall()

        cur.execute(query_results)
        results: List[Tuple[Union[str, int]]] = cur.fetchall()

        cur.execute(query_count)
        count: int = cur.fetchone()[0]

        print('number of register for this query:: ', count)

        data = DataFrame.from_records(data=results,
                                      columns=[column[1] for column in columns])

        if data.empty:
            print('Nothing to show')
            return

        print(data)

    except sqlite3.OperationalError as e:
        error = f'We can\'t perform this action because the table {TABLE_NAME} does not exists'
        print('This is the real error')
        print(e)
        print(f'error {error}')
        cur.close()


def list_by_date_and_value(cur: Cursor, con: Connection, args: Namespace):
    pass
