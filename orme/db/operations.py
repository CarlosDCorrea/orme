import sqlite3
from sqlite3 import Cursor, Connection
from typing import List, Tuple, Union

from pandas import DataFrame


def create(cur: Cursor, con: Connection, queries: List[str], table_name: str) -> None:
    create_table_query, insert_into_query = queries[0], queries[1]

    cur.execute(create_table_query)
    cur.execute(insert_into_query)
    con.commit()
    cur.close()

    print(f'Register created in table {table_name} successfully')


def list_(cur: Cursor, queries: List[str], table_name: str) -> None:
    query_results = queries[0]
    query_count = queries[1]

    get_table_columns_query = f'PRAGMA table_info({table_name})'

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

        print(
            f'number of register for this query in table {table_name} {count}')

        data = DataFrame.from_records(data=results,
                                      columns=[column[1] for column in columns])

        if data.empty:
            print('Nothing to show')
            return

        print(data)

    except sqlite3.OperationalError as e:
        error = f'We can\'t perform this action because the table {table_name} does not exists'
        print('This is the real error')
        print(e)
        print(f'error {error}')
        cur.close()


def update(cur: Cursor, con: Connection, queries: List[str]) -> None:
    update_query = queries[0]
    print(f'update query {update_query}')
    cur.execute(update_query)
    con.commit()
    cur.close()

    print('Registro actualizado satisfactoriamente')


def delete(cur: Cursor, con: Connection, queries: List[str]) -> None:
    delete_query = queries[0]

    cur.execute(delete_query)
    con.commit()
    cur.close()

    print('Registro eliminado satisfactoriamente')


def total(cur: Cursor, queries: List[str]) -> None:
    total_expenses_value_query: str = queries[0]
    count_registers: str = queries[1]

    print(total_expenses_value_query)
    print(count_registers)
    cur.execute(total_expenses_value_query)
    result: int | None = cur.fetchone()[0]

    cur.execute(count_registers)
    count: int = cur.fetchone()[0]

    if count:
        print(f'{count} expenses found for today with a total value of {result}')
        return

    print('No data found')
