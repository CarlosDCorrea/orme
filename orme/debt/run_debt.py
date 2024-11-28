from argparse import Namespace
from typing import Tuple, List

from orme.utils import get_present_arguments

from orme.db.queries.common_queries import (generate_insert_into_query,
                                            generate_list_query,
                                            generate_update_query,
                                            generate_delete_query,
                                            generate_get_query)
from orme.db.connection import create_connection_and_execute_query


TABLE_NAME = 'debts'


def create_debt(args: Namespace) -> None:
    queries: List[str] = generate_insert_into_query(args)
    create_connection_and_execute_query(
        'create', queries, TABLE_NAME)


def list_debts(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = generate_list_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'list', queries, 'debts')


def update_debt(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    if len(present_arguments) == 1:
        raise ValueError('This command requires the fields to be updated')

    queries: List[str] = generate_update_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'update', queries, 'debts')


def delete_debt(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = generate_delete_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'delete', queries, 'debts')


def get_debt(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    # lets just work with it for now
    queries: List[str] = generate_get_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'get', queries, 'debts'
    )


""" def proyection(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    create_connection_and_execute_query(
        'get', queries, 'debts'
    )

    print(f'results: {results}') """
