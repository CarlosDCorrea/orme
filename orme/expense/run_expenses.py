from datetime import date
from argparse import Namespace
from typing import Tuple, List, Dict

from orme.utils import get_present_arguments, get_dict_present_arguments

from orme.db.connection import create_connection_and_execute_query

from orme.db.queries.common_queries import (generate_insert_into_query,
                                            generate_list_query,
                                            generate_update_query,
                                            generate_delete_query,
                                            generate_total_query)


TABLE_NAME = 'expenses'


def create_expense(args: Namespace) -> None:
    present_arguments: Dict[str, str | int | List[str | int]] = get_dict_present_arguments(args)
    today: str = date.today().isoformat()

    if 'div' in args:
        is_divided: int = 1 if present_arguments['div'] else 0
        del present_arguments['div']
        present_arguments['is_divided'] = is_divided

    present_arguments['created'] = today
    present_arguments['updated'] = today

    queries: List[str] = generate_insert_into_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'create', queries, TABLE_NAME)


def list_expenses(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    queries = generate_list_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'list', queries, TABLE_NAME)


def update_expense(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)

    print('inside update expense')
    if len(present_arguments) == 1:
        print('throwing exception')
        raise ValueError('This command requires the fields to be updated')

    queries = generate_update_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'update', queries, TABLE_NAME)


def delete_expense(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    queries = generate_delete_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'delete', queries, TABLE_NAME)


def total(args: Namespace) -> None:
    present_arguments: List[Tuple] = get_present_arguments(args)
    queries = generate_total_query(present_arguments, TABLE_NAME)
    create_connection_and_execute_query(
        'total', queries, TABLE_NAME)
