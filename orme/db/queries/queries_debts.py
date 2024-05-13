from argparse import Namespace
from datetime import date
from typing import List, Tuple, Union

from orme.db.common import generate_sql_where_by_operator


TABLE_NAME = 'debts'


def generate_create_query(args: Namespace) -> Tuple[str]:
    today: str = date.today().isoformat()

    create_debts_table_query: str = f"""
    CREATE TABLE if not exists {TABLE_NAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        deptor TEXT,
        lender TEXT,
        description TEXT,
        interest_rate INTEGER NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
    """

    insert_into_debts_query = f"""
    INSERT INTO {TABLE_NAME}(
        value,
        deptor,
        lender,
        description,
        interest_rate,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.deptor}',
            '{args.lender}',
            '{args.description}',
            {args.interest_rate},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    return (create_debts_table_query, insert_into_debts_query)


def generate_list_query(args: List[Tuple[str, Union[str | int]]]) -> Tuple[str]:
    offset = 0
    limit = 10

    where_statement: str = ''

    if args:
        where_statement = generate_sql_where_by_operator(args)

    # NOTICE: The blank spaces could be a problem when evaluating the query
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


def generate_update_query():
    pass


def generate_delete_query():
    pass
