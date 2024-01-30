from ..db.connection import create_connection_and_execute_query


TABLE_NAME = 'expenses'


def create_expense(args):
    create_connection_and_execute_query(TABLE_NAME, 'create', args)


def list_expenses(args):
    create_connection_and_execute_query(TABLE_NAME, 'list', args)


def generate_graph(args):
    pass


def generate_stats(args):
    pass
