from argparse import Namespace
from datetime import date
from typing import Tuple


TABLE_NAME = 'expenses'


def generate_create_query(args: Namespace) -> Tuple[str, str]:
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

    insert_into_expenses_query = f"""
    INSERT INTO {TABLE_NAME}(
        value,
        user,
        category,
        description,
        is_divided,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.user}',
            '{args.category}',
            '{args.description}',
            {is_divided},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    return (insert_into_expenses_query,)
