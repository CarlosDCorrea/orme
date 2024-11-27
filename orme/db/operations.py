import sqlite3
import shutil
from sqlite3 import Cursor, Connection
from typing import List, Tuple, Union

import pandas as pd


def create(cur: Cursor, con: Connection, queries: List[str], table_name: str) -> None:
    create_query = queries[0]
    cur.execute(create_query)

    con.commit()
    cur.close()

    if table_name != 'migrations':
        print(f'Register created in table {table_name} successfully')


def list_(cur: Cursor, queries: List[str], table_name: str) -> None:
    query_results = queries[0]
    query_count = queries[1]

    get_table_columns_query = f'PRAGMA table_info({table_name})'
    offset: int = 0

    try:
        cur.execute(get_table_columns_query, ())
        columns: List[Tuple[Union[int, str]]] = cur.fetchall()
        n_cols: int = len([column[1] for column in columns])

        # Some value of the last column could be out of bound, ending up in an overflow to the line below
        # thats why the substraction of - 1 for each column
        col_size: int = (shutil.get_terminal_size().columns // n_cols) - 1

        cur.execute(query_count)
        count: int = cur.fetchone()[0]

        if not count:
            print('No data found')
            return

        limit: int = 10 if count > 10 else count
        remaining: int = 0 if not (count - limit) else count - limit

        print(
            f'number of register for this query in table {table_name} {count}')

        while True:
            # print('starting with offset {} and limit {} and remaining {}'.format(offset, limit, remaining))
            # TODO: use pandas sql reader instead of cur to retrieve the rows
            # get the requested data
            cur.execute(query_results, (offset, limit))
            results: List[Tuple[Union[str, int]]] = cur.fetchall()

            df = pd.DataFrame.from_records(data=results,
                                           columns=[column[1] for column in columns])

            if df.empty and not offset:
                print('Nothing to show')
                return
            elif df.empty:
                print('Nothing more to show')
                return

            if offset:
                # if there is more data to show, shell cursor goes 1 line up and ...
                print('\033[A\033[K', end='\n')
                print(df[:offset].to_string(index=False,
                                            header=False,
                                            max_colwidth=col_size,
                                            col_space=col_size))
            else:
                print(df.to_string(index=False,
                                   max_colwidth=col_size,
                                   col_space=col_size))

            while True:
                try:
                    user_input = input(f'({remaining}):')
                except KeyboardInterrupt:
                    return
                if user_input == 'q':
                    return
                elif user_input == '':
                    break
                else:
                    continue

            offset, limit = offset + limit, remaining if remaining < limit else limit
            remaining -= limit
            # print('finishing with offset {} and limit {} and remaining {}'.format(offset, limit, remaining))

    except sqlite3.OperationalError as e:
        print(e)
        cur.close()


def update(cur: Cursor, con: Connection, queries: List[str]) -> None:
    update_query = queries[0]
    cur.execute(update_query)
    con.commit()

    if cur.rowcount:
        print('Registro actualizado satisfactoriamente')
    else:
        print('No register found with the specified id')

    cur.close()


def delete(cur: Cursor, con: Connection, queries: List[str]) -> None:
    delete_query = queries[0]

    cur.execute(delete_query)
    con.commit()

    if cur.rowcount > 0:
        print('Register deleted')
    else:
        print('No registers found to delete')

    cur.close()


def total(cur: Cursor, queries: List[str]) -> None:
    total_expenses_value_query: str = queries[0]
    count_registers: str = queries[1]

    cur.execute(total_expenses_value_query)
    result: int | None = cur.fetchone()[0]

    cur.execute(count_registers)
    count: int = cur.fetchone()[0]

    if count:
        print(f'{count} expenses found with a total value of {result}')
        return

    print('No data found')


def get(cur: Cursor, queries: List[str]) -> None | Tuple[str | int]:
    get_query = queries[0]

    cur.execute(get_query)
    result = cur.fetchone()

    cur.close()
    return result
