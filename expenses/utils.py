from ..validations import validate_date


def create_list_expense_query(args) -> None | str:
    query = ''
    date = ''
    operator = None
    table_name = 'expenses'

    if args.ltd:
        date = args.ltd
        operator = '<='
    elif args.gtd:
        date = args.gtd
        operator = '>='
    elif args.date:
        date = args.date
        operator = '='
    else:
        query = f"SELECT * FROM {table_name} ORDER BY date DESC"
        return query

    validate_date(date)

    query = f"SELECT * FROM {table_name} WHERE date {operator} Date('{date}') ORDER BY date DESC"
    print('final query ', query)
    return query
