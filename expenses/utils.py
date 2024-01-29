import types
from argparse import Namespace
from typing import DefaultDict, Union, List
from collections import defaultdict


def get_present_arguments(args: Namespace) -> List[tuple]:
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    return present_arguments


def create_list_expense_query(args: Namespace) -> None | str:
    # get only the arguments that the user enter (e.g argument != None) and is not a function
    present_arguments = get_present_arguments(args)

    # TODO how should validate date string? and check sqlite docs about operators with dates
    match present_arguments:
        case [('gtd', value)]:
            where_statement = f"""> '{value}'"""
            column = 'date'
        case [('ltd', value)]:
            where_statement = f"""< '{value}'"""
            column = 'date'
        case [('gtd', start_value), ('ltd', end_value)]:
            where_statement = f"""BETWEEN '{start_value}' AND '{end_value}'"""
            column = 'date'
        case [('date', value)]:
            where_statement = f"""= '{value}'"""
            column = 'date'
        case [('gtv', value)]:
            where_statement = f"""> '{value}'"""
            column = 'value'
        case [('ltv', value)]:
            where_statement = f"""< '{value}'"""
            column = 'value'
        case [('gtv', start_value), ('ltv', end_value)]:
            where_statement = f"""BETWEEN '{start_value}' AND '{end_value}'"""
            column = 'value'
        case [('value', value)]:
            where_statement = f"""= '{value}'"""
            column = 'value'
        case _:
            where_statement = ''

    return _list() if not where_statement else _list_with_filters(column, where_statement)


def _list(offset=0, limit=10, table_name='expenses') -> str:
    result: DefaultDict[str, str] = defaultdict(Union[str, int])

    query_results = f"""
            SELECT *
            FROM expenses
            ORDER BY date DESC
            LIMIT {offset}, {limit}
            """

    query_count = """
            SELECT COUNT(*)
            FROM expenses
            """

    result['query_results'] = query_results
    result['query_count'] = query_count
    result['offset'] = offset
    result['limit'] = limit

    return result


def _list_with_filters(column: str, where_statement: str, offset: int = 0, limit: int = 10) -> None:
    query = f"""
            SELECT *
            FROM expenses
            WHERE {column} {where_statement}
            ORDER BY date DESC
            LIMIT {offset}, {limit}
            """

    return query
