import types


def create_list_expense_query(args) -> None | str:
    # get only the arguments that the user enter (e.g argument != None) and is not a function
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    # TODO how should validate date string? and check sqlite docs about operators with dates
    match present_arguments:
        case [('gtd', value)]:
            where_statement = f""">= '{value}'"""
        case [('ltd', value)]:
            where_statement = f"""<= '{value}'"""
        case [('gtd', start_date), ('ltd', end_date)]:
            where_statement = f"""BETWEEN '{start_date}' AND '{end_date}'"""
        case [('date', value)]:
            where_statement = f"""= '{value}'"""
        case _:
            where_statement = ''

    return _list() if not where_statement else _list_by_date(where_statement)


def _list(offset=0, limit=10, table_name='expenses') -> str:
    query = f"""
            SELECT *
            FROM expenses
            ORDER BY date DESC
            LIMIT {offset}, {limit}
    """
    return query


def _list_by_date(where_statement):
    query = f"""
            SELECT *
            FROM expenses
            WHERE date {where_statement}
            """

    print(f"query {query}")
    return query


def _list_by_value(date=True, gtd=False, ltd=False):
    pass
