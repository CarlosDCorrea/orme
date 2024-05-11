from argparse import Namespace
from datetime import date
from typing import Tuple, List, Union

from ..utils import get_present_arguments, get_operator

from ..validations import validate_date

from ..db.queries.common import generate_sql_where_by_operator

QUERY_CREATE = 1
QUERY_LIST = 2
QUERY_UPDATE = 3
QUERY_DELETE = 4

TABLE_NAME = 'debts'


def generate_create_query(args: List[Tuple]) -> Tuple[str]:
    validate_date(args.date)
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

    operator: str | None = get_operator(args)

    where_statement = generate_sql_where_by_operator(operator, args[0]) if operator else ''

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


def define_query(query_type: int, args: Namespace) -> str:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = []

    if query_type == QUERY_CREATE:
        queries = generate_create_query(present_arguments)
    if query_type == QUERY_LIST:
        queries = generate_list_query(present_arguments)
    if query_type == QUERY_UPDATE:
        pass
    if query_type == QUERY_DELETE:
        pass

    return queries


def create_debt(args):
    pass


def list_debts(args: Namespace) -> None:
    print(define_query(QUERY_LIST, args))
