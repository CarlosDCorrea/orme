from typing import List, Tuple, Union


def generate_sql_where_by_operator(args: List[Tuple[str, Union[str, int]]]) -> str:
    where_statement = 'WHERE '
    common_operators = ['<=', '>=', '=']

    for arg in args:
        if where_statement != 'WHERE ':
            where_statement += 'AND'

        operator = get_operator(arg[0])
        field = get_field_name(arg[0])

        values: Union[str, int, List[Union[str, int]]] = arg[1]
        if operator in common_operators:
            where_statement += f'{field} {operator} {values}'
        elif operator == '><':
            where_statement += f'{field} BETWEEN {values[0]} AND {values[1]}'
    return where_statement


def get_operator(arg: str) -> str | None:
    match arg:
        case arg if arg.startswith('bt'):
            return '><'
        case arg if arg.startswith('gt'):
            return '>='
        case arg if arg.startswith('lt'):
            return '<='
        case arg if arg.startswith('eq'):
            return '='
        case _:
            return None


def get_field_name(arg: str) -> str | None:
    match arg:
        case arg if arg.endswith('v'):
            return 'value'
        case arg if arg.endswith('d'):
            return 'date'
        case _:
            return None
