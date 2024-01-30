from argparse import Namespace
from sqlite3 import Cursor, Connection
from datetime import date

from ...validations import validate_date


def create(cur: Cursor, con: Connection, args: Namespace):
    validate_date(args.date)
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

    cur = con.cursor()

    create_expenses_table_query = """
    CREATE TABLE if not exists expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value INTEGER NOT NULL,
        user TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        is_divided INTEGER NOT NULL,
        date TEXT,
        created TEXT,
        updated TEXT
        )
    """

    insert_into_expenses_query = f"""
    INSERT INTO expenses(
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

    cur.execute(create_expenses_table_query)
    cur.execute(insert_into_expenses_query)
    con.commit()
    cur.close()

    print('The expense was registered successfully...')