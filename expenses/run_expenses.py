import sqlite3
from datetime import date

from pandas import DataFrame

from ..validations import validate_date
from ..settings import DATABASE_URL
from .utils import create_list_expense_query


def create_expense(args):
    validate_date(args.date)
    today = date.today().isoformat()
    is_divided = 1 if args.div else 0

    with sqlite3.connect(DATABASE_URL) as con:
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


def list_expenses(args):
    table_name = 'expenses'
    with sqlite3.connect(DATABASE_URL) as conn:
        cur = conn.cursor()
        list_expenses_query = create_list_expense_query(args)

        get_table_columns_query = f'PRAGMA table_info({table_name})'

        try:
            # get the table columns
            cur.execute(get_table_columns_query)
            columns = cur.fetchall()
            cur.execute(list_expenses_query)
            results = cur.fetchall()

            data = DataFrame.from_records(data=results,
                                          columns=[column[1] for column in columns])

            if data.empty:
                print('Nothing to show')
                return

            print(data)
        except sqlite3.OperationalError as e:
            error = f'We can\'t perform this action because the table {table_name} does not exists'
            print('This is the real error')
            print(e)
            print(f'error {error}')
        finally:
            cur.close()


def generate_graph(args):
    pass


def generate_stats(args):
    pass
