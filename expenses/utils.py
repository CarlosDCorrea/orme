import types
from argparse import Namespace
from typing import DefaultDict, Union, List, Tuple
from collections import defaultdict


def get_present_arguments(args: Namespace) -> List[Tuple]:
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    return present_arguments


def create_list_expense_query(args: Namespace, must_increment: bool) -> None | str:
    # get only the arguments that the user enter (e.g argument != None) and is not a function
    present_arguments: List[Tuple] = get_present_arguments(args)
    where_statements: List[Tuple[str]] = []
    # where_statement: str = ''

    # TODO how should validate date string? and check sqlite docs about operators with dates
    match present_arguments:
        case [('gtd', value)]:
            where_statements.append((f"""> '{value}'""", 'date'))
        case [('ltd', value)]:
            where_statements.append((f"""< '{value}'""", 'date'))
        case [('gtd', start_value), ('ltd', end_value)]:
            where_statements.append()(
                f"""BETWEEN '{start_value}' AND '{end_value}'""", 'date')
        case [('date', value)]:
            where_statements.append((f"""= '{value}'""", 'date'))
        case [('gtv', value)]:
            where_statements.append((f"""> '{value}'""", 'value'))
        case [('ltv', value)]:
            where_statements.append((f"""< '{value}'""", 'value'))
        case [('gtv', start_value), ('ltv', end_value)]:
            where_statements.append(
                (f"""BETWEEN '{start_value}' AND '{end_value}'""", 'value'))
        case [('value', value)]:
            where_statements.append((f"""= '{value}'""", 'value'))
        case _:
            return _list(must_increment)

    """ For now it is assume that in every iteration the field is different.
    NOTE: it does not work because a patter to accepting different arguments
    is not supported therefore _list() ends up been invocated.
    The tuple sintax is going to be conservated for future analisys of multiple
    arguments support"""
    """ count: int = 0
    for statement in where_statements:
        if count:
            where_statement += 'AND'

        where_statement += f'{statement[1]} {statement[0]}'
        count += 1

    print('query_statements')
    print(where_statements)
    return _list_with_filters(where_statement) """


def _list(offset=0, limit=1, table_name='expenses', must_increment=False) -> DefaultDict[str, Union[str, int]]:
    result: DefaultDict[str, Union[str, int]] = defaultdict(Union[str, int])
    if must_increment:
        offset = limit
        limit += 1

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


def _list_with_filters(where_statements: List[Tuple[str]], offset: int = 0, limit: int = 10) -> None:
    query = f"""
            SELECT *
            FROM expenses
            WHERE {where_statements[0][1]} {where_statements[0][0]}
            ORDER BY date DESC
            LIMIT {offset}, {limit}
            """

    return query
