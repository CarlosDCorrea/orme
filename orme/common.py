from typing import List, Tuple


def generate_sql_where_by_operator(data: List[Tuple[str, str, str | int]]) -> str:
    where_statement = 'WHERE '
    common_operators = ['<=', '>=', '=']

    for record in data:
        if where_statement != 'WHERE ':
            where_statement += 'AND'

        field_name, operator, values = record

        if operator in common_operators:
            if isinstance(values, str):
                values = f"'{values}'"
            where_statement += f'{field_name} {operator} {values}'
        elif operator == '><':
            if isinstance(values[0], str):
                values[0], values[1] = f"'{values[0]}'", f"'{values[1]}'"
            where_statement += f"{field_name} BETWEEN {values[0]} AND {values[1]}"
    return where_statement


def get_operator(command: str) -> str | None:
    match command:
        case command if command.startswith('between'):
            return '><'
        case command if command.startswith('greater'):
            return '>='
        case command if command.startswith('less'):
            return '<='
        case command if command.startswith('equal'):
            return '='


def get_field_name(command: str) -> str | None:
    match command:
        case command if command.endswith('value'):
            return 'value'
        case command if command.endswith('date'):
            return 'date'
