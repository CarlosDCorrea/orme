from argparse import Namespace
from datetime import date
from typing import Tuple


TABLE_NAME = 'debts'


def generate_create_query(args: Namespace) -> Tuple[str, str]:
    today: str = date.today().isoformat()

    insert_into_debts_query = f"""
    INSERT INTO {TABLE_NAME}(
        value,
        deptor,
        lender,
        description,
        interest_rate,
        months,
        date,
        created,
        updated) VALUES(
            {args.value},
            '{args.deptor}',
            '{args.lender}',
            '{args.description}',
            {args.interest_rate},
            {args.months},
            '{args.date}',
            '{today}',
            '{today}'
            )"""

    return (insert_into_debts_query,)
