import sqlite3
from typing import DefaultDict, Union, Tuple, List

from pandas import DataFrame

from ..settings import DATABASE_URL
from .utils import create_list_expense_query
from ..db.connection import create_connection_and_execute_query


TABLE_NAME = 'expenses'


def create_expense(args):
    create_connection_and_execute_query(TABLE_NAME, 'create', args)


def list_expenses(args):
    TABLE_NAME = 'expenses'
    is_finished: bool = False

    must_increment: bool = False
    with sqlite3.connect(DATABASE_URL) as conn:
        cur = conn.cursor()

        while not is_finished:
            # Create the query based in the args
            # query_results
            # query_count
            # offset
            # limit     
            result: DefaultDict[str, Union[str, int]
                                ] = create_list_expense_query(args, must_increment)

            print(result)

            get_table_columns_query = f'PRAGMA table_info({TABLE_NAME})'

            try:
                # is the first time that this executes
                if not must_increment:
                    # get the table columns
                    cur.execute(get_table_columns_query)
                    columns = cur.fetchall()

                    # TODO: use pandas sql reader instead of cur to retrieve the rows
                    # get the requested data
                    cur.execute(result['query_results'])
                    results: List[Tuple[Union[str, int]]] = cur.fetchall()

                    # get the count of the table's rows
                    cur.execute(result['query_count'])
                    count: int = cur.fetchone()[0]
                else:
                    results.extend(cur.execute(result['query_results']))
                # TODO thing about how to implement the 'load more data'
                # but later, implement first the core functionality
                print(result)
                data = DataFrame.from_records(data=results,
                                              columns=[column[1] for column in columns])

                if data.empty:
                    print('Nothing to show')
                    return

                print(data)

                if len(results) == count:
                    is_finished = True
                else:
                    user_input = input('Show more:')
                    if not user_input:
                        must_increment = True
                    if user_input == 'q':
                        is_finished = True

            except sqlite3.OperationalError as e:
                error = f'We can\'t perform this action because the table {TABLE_NAME} does not exists'
                print('This is the real error')
                print(e)
                print(f'error {error}')
                cur.close()

        cur.close()


def generate_graph(args):
    pass


def generate_stats(args):
    pass
