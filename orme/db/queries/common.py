from typing import Tuple, Union


def generate_sql_where_by_operator(operator: str, values: Tuple[str, Union[str | int]], field: str) -> str:
    where_statement = 'WHERE '

    common_operators = ['<', '>', '=']

    if operator in common_operators:
        return where_statement + f'{field} {operator} {values[0]}'

    return where_statement + f'{field} BETWEEN {values[0]} AND {values[1]}'
