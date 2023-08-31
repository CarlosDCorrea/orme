import argparse
import sqlite3
from datetime import date


parser = argparse.ArgumentParser(
                    prog="Orme",
                    description="This program allows the user to register all its expenses",
                    epilog="TechSsus - Carlos Correa"   
                 )

""" Global arguments
- expense 
   - add
   - edit
   - delete
"""
subparsers = parser.add_subparsers(required=True)
""" add Sub Argument
Add something
"""
parser_add = subparsers.add_parser('add', help='adds a new expense with all its attributes')
parser_add.add_argument('type', help='the type of register to add', choices=['expense', 'income'])
#parser_expense.add_argument('date', type=str, help='The date of this particular expense (not the register)')
#parser_expense.add_argument('desc', type=str, help='The description of this particular expense')

args = vars(parser.parse_args())
print('args::', args)

con = sqlite3.connect('orme.db')
cur = con.cursor()

cur.execute('CREATE TABLE if not exists expenses(value)')

cur.execute(f"""INSERT INTO expenses VALUES({args['val']})""")

con.commit()

cur.close()
con.close()