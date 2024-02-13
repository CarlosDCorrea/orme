import sqlite3
from argparse import Namespace
from typing import List, Tuple

from ..settings import DATABASE_URL
from .queries.queries_expenses import create, list_, list_by_date, list_by_value
from ..utils import get_present_arguments


def create_connection_and_execute_query(table_name: str, operation: str, args: Namespace, **kargs: object):
    with sqlite3.connect(DATABASE_URL) as con:
        cur = con.cursor()

        if operation == 'create':
            create(cur, con, args)

        if operation == 'list':
            present_arguments: List[Tuple] = get_present_arguments(args)
            where_statement: str = ''

            match present_arguments:
                case [('gtd', value)]:
                    where_statement = f"""> '{value}'"""
                    list_by_date(cur, con, where_statement)
                case [('ltd', value)]:
                    where_statement = f"""< '{value}'"""
                    list_by_date(cur, con, where_statement)
                case [('gtd', start_value), ('ltd', end_value)]:
                    where_statement = f"""BETWEEN '{start_value}' AND '{end_value}'"""
                    list_by_date(cur, con, where_statement)
                case [('date', value)]:
                    where_statement = f"""= '{value}'"""
                    list_by_date(cur, con, where_statement)
                case [('gtv', value)]:
                    where_statement = f"""> '{value}'"""
                    list_by_value(cur, con, where_statement)
                case [('ltv', value)]:
                    where_statement = f"""< '{value}'"""
                    list_by_value(cur, con, where_statement)
                case [('gtv', start_value), ('ltv', end_value)]:
                    where_statement = f"""BETWEEN '{start_value}' AND '{end_value}'"""
                    list_by_value(cur, con, where_statement)
                case [('value', value)]:
                    where_statement = f"""= '{value}'"""
                    list_by_value(cur, con, where_statement)
                case _:
                    list_(cur, con)

        cur.close()
        print('cur closed')

    print('connection closed')


def execute_command():
    pass
