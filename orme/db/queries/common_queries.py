from argparse import Namespace
from datetime import date
from typing import List, Tuple

from orme.db.common import generate_sql_where_by_operator
from orme.expenses.utils import generate_dateframe


# TODO: see if this abstraction is neccesary, create will be unique for every type of operation (debt, expense)
def generate_create_query(args: Namespace, table_name: str, fields: List[str], values: str) -> Tuple[str]:
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


def generate_list_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str]:
    offset = 0
    limit = 10

    where_statement: str = ''

    if args:
        where_statement = generate_sql_where_by_operator(args)

    query_results = f"""
                    SELECT * FROM {table_name}
                    {where_statement}
                    ORDER BY date DESC
                    LIMIT {offset}, {limit}
                    """

    query_count = f"""
                   SELECT COUNT(*)
                   FROM {table_name}
                   {where_statement}
                   """

    return (query_results, query_count)


def generate_update_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str]:
    """ NOTE: for now we are not going to support updating for several registers, thus
    generate_sql_where_by_operator is not neccesary """

    today = date.today().isoformat()

    update_table_query = f"""
    UPDATE {table_name}
    SET {", ".join([" = ".join([f"'{item}'" for item in arg]) for arg in args[1:]])}, updated = '{today}'
    WHERE {" = ".join([str(item) for item in args[0]])}"""

    return (update_table_query,)


def generate_delete_query(args: List[Tuple[str, str | int]], table_name) -> Tuple[str]:
    delete_expense_query = f"""
    DELETE FROM {table_name}
    WHERE {"=".join([str(item) for item in args[0]])}"""

    return (delete_expense_query,)


def generate_total_query(args: List[Tuple[str, str]], table_name) -> Tuple[str]:
    local_args: List[Tuple[str, str | List[str]]] = generate_dateframe(args)
    where_statement = generate_sql_where_by_operator(local_args)

    total_expenses_value_query: str = f"""
    SELECT SUM(value) FROM {table_name}
    {where_statement}"""

    count_registers: str = f"""
    SELECT COUNT(*)
    FROM {table_name}
    {where_statement}"""

    return (total_expenses_value_query, count_registers)
