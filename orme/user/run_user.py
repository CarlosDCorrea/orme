from datetime import date
from argparse import Namespace
from typing import Tuple, List, Dict

from orme.utils import get_present_arguments, get_dict_present_arguments

from orme.db.queries.common_queries import (generate_insert_into_query,
                                            generate_list_query,
                                            generate_update_query,
                                            generate_delete_query,
                                            generate_get_query)
from orme.db.connection import create_connection_and_execute_query


TABLE_NAME = 'users'


def create_user(args: Namespace) -> None:
    present_arguments: Dict[str, str | int | List[str | int]] = get_dict_present_arguments(args)
    today: str = date.today().isoformat()

    present_arguments['created'] = today
    present_arguments['updated'] = today

    queries: List[str] = generate_insert_into_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'create', queries, TABLE_NAME)


def list_users(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    queries: List[str] = generate_list_query(present_arguments, TABLE_NAME)

    create_connection_and_execute_query(
        'list', queries, TABLE_NAME)


def update_user(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    if len(present_arguments) == 1:
        raise ValueError('This command requires the fields to be updated')

    queries: List[str] = generate_update_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'update', queries, TABLE_NAME)


def delete_user(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    queries: List[str] = generate_delete_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'delete', queries, TABLE_NAME)


def get_user(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    # lets just work with it for now
    queries: List[str] = generate_get_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'get', queries, TABLE_NAME
    )
