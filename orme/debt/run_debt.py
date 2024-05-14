from argparse import Namespace
from typing import Tuple, List

from orme.utils import get_present_arguments

from orme.db.queries.queries_debts import generate_create_query, generate_list_query
from orme.db.connection import create_connection_and_execute_query
from orme.settings import (QUERY_CREATE,
                           QUERY_LIST,
                           QUERY_UPDATE,
                           QUERY_DELETE)


TABLE_NAME = 'debts'


def define_query(query_type: int, args: Namespace) -> str:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = []

    if query_type == QUERY_CREATE:
        print(present_arguments)
        queries = generate_create_query(args)
    if query_type == QUERY_LIST:
        queries = generate_list_query(present_arguments)
    if query_type == QUERY_UPDATE:
        pass
    if query_type == QUERY_DELETE:
        pass

    return queries


def create_debt(args):
    create_connection_and_execute_query(
        'create', define_query(QUERY_CREATE, args), TABLE_NAME)


def list_debts(args: Namespace) -> None:
    create_connection_and_execute_query(
        'list', define_query(QUERY_LIST, args), 'debts')


def update_debt(args: Namespace) -> None:
    create_connection_and_execute_query(
        'update', define_query(QUERY_UPDATE, args), 'debts')


def delete_debt(args: Namespace) -> None:
    create_connection_and_execute_query(
        'delete', define_query(QUERY_DELETE, args), 'debts')
