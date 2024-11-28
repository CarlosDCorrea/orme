from datetime import date
from typing import List, Tuple, Dict

from orme.common import generate_sql_where_by_operator
from ...common import get_operator, get_field_name
from orme.expense.utils import generate_dateframe


def generate_insert_into_query(data: Dict[str, Tuple[str | int]], table_name):
    character = ', \n'
    insert_into: str = f"""
    INSERT INTO {table_name}(
        {character.join(data)}) VALUES(
        {character.join([f"'{value}'"
                         if isinstance(value, str)
                         else str(value)
                         for value in data.values()])}
            );"""

    return (insert_into,)


def generate_list_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str, str]:
    where_statement: str = ''

    data: List[Tuple[str, str, str | int | List[str | int]]] = []

    if args:
        for arg in args:
            command: str = arg[0]
            values: str | int | List[str | int] = arg[1]
            field_name: str = get_field_name(command)
            operator: str = get_operator(command)

            data.append((field_name, operator, values))

        where_statement = generate_sql_where_by_operator(data)

    query_results = f"""
                    SELECT * FROM {table_name}
                    {where_statement}
                    ORDER BY date DESC
                    LIMIT ?, ?
                    """

    query_count = f"""
                   SELECT COUNT(*)
                   FROM {table_name}
                   {where_statement}
                   """

    return (query_results, query_count)


def generate_update_query(args: List[Tuple[str, str | int]], table_name: str) -> Tuple[str]:
    today = date.today().isoformat()

    update_table_query = f"""
    UPDATE {table_name}
    SET {", ".join(
        [" = ".join(
            [f"'{item}'" for item in arg])
                         for arg in args[1:]])}, updated = '{today}'
    WHERE {" = ".join([str(item) for item in args[0]])}"""

    return (update_table_query,)


def generate_delete_query(args: List[Tuple[str, str | int]], table_name) -> Tuple[str]:
    delete_query = f"""
    DELETE FROM {table_name}
    WHERE {"=".join([item for item in args[0]])}"""

    return (delete_query,)


def generate_total_query(args: List[Tuple[str, str]], table_name) -> Tuple[str]:
    local_args: List[Tuple[str, str | List[str]]] = generate_dateframe(args)
    where_statement: str = ''

    if local_args:
        where_statement = generate_sql_where_by_operator(local_args)

    total_value_query: str = f"""
    SELECT SUM(value) FROM {table_name}
    {where_statement}"""

    count_registers: str = f"""
    SELECT COUNT(*)
    FROM {table_name}
    {where_statement}"""

    return (total_value_query, count_registers)


def generate_get_query(args: List[Tuple[str, str]], table_name) -> Tuple[str]:
    field: str = args[0][0]
    value: int = args[0][1]

    where_statement = f'WHERE {field} == {value}'
    get_query: str = f"""
    SELECT * FROM {table_name}
    {where_statement}"""

    return (get_query,)
