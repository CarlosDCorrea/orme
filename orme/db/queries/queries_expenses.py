from argparse import Namespace
from datetime import date
from typing import Union, List, Tuple
from orme.db.common import generate_sql_where_by_operator


TABLE_NAME = 'expenses'


get_table_columns_query = f'PRAGMA table_info({TABLE_NAME})'


def generate_create_query(args: Namespace) -> Tuple[str]:
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

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

    return (create_expenses_table_query, insert_into_expenses_query)


def generate_list_query(args: List[Tuple[str, Union[str | int]]]) -> Tuple[str]:
    offset = 0
    limit = 10

    where_statement: str = ''

    if args:
        where_statement = generate_sql_where_by_operator(args)

    query_results = f"""
                    SELECT * FROM {TABLE_NAME}
                    {where_statement}
                    ORDER BY date DESC
                    LIMIT {offset}, {limit}
                    """

    query_count = f"""
                   SELECT COUNT(*)
                   FROM {TABLE_NAME}
                   {where_statement}
                   """

    return (query_results, query_count)
