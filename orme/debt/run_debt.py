from argparse import Namespace
from typing import Tuple, List

from orme.utils import get_present_arguments

from orme.db.queries.common_queries import (generate_list_query,
                                            generate_update_query,
                                            generate_delete_query,
                                            generate_get_query)
from orme.db.connection import create_connection_and_execute_query
from orme.settings import (QUERY_CREATE,
                           QUERY_LIST,
                           QUERY_UPDATE,
                           QUERY_DELETE,
                           QUERY_GET)


TABLE_NAME = 'debts'


def define_query(query_type: int, args: Namespace) -> str:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = []

    if query_type == QUERY_CREATE:
        with open('sql/create_debts.sql', 'r') as create_query, \
             open('sql/insert_debt.sql', 'r') as insert_query:
            queries = [create_query.read(), insert_query.read()]

    if query_type == QUERY_LIST:
        queries = generate_list_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_UPDATE:
        if len(present_arguments) == 1:
            raise ValueError('This command requires the fields to be updated')
        queries = generate_update_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_DELETE:
        queries = generate_delete_query(present_arguments, TABLE_NAME)
    if query_type == QUERY_GET:
        queries = generate_get_query(present_arguments, TABLE_NAME)

    return queries


def create_debt(args: Namespace) -> None:
    create_connection_and_execute_query(
        'create', define_query(QUERY_CREATE, args), TABLE_NAME)


def list_debts(args: Namespace) -> None:
    create_connection_and_execute_query(
        'list', define_query(QUERY_LIST, args), 'debts')


def update_debt(args: Namespace) -> None:
    try:
        create_connection_and_execute_query(
            'update', define_query(QUERY_UPDATE, args), 'debts')
    except ValueError as e:
        print(e)


def delete_debt(args: Namespace) -> None:
    create_connection_and_execute_query(
        'delete', define_query(QUERY_DELETE, args), 'debts')


def get_debt(args: Namespace) -> None:
    # lets just work with it for now
    result = create_connection_and_execute_query(
        'get', define_query(QUERY_GET, args), 'debts'
    )

    print(result)


def proyection(args: Namespace) -> None:
    results = create_connection_and_execute_query(
        'get', define_query(QUERY_GET, args), 'debts'
    )

    print(f'results: {results}')
