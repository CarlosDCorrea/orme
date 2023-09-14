import argparse
import sqlite3
from datetime import date


def validate_date(str_date):
   try:
      date.fromisoformat(str_date)
   except ValueError as e:
      print(e)

def list_expenses(args):
   print('running list expenses method', args.type)

def run_list_expenses(subparser):
   parser_list = subparsers.add_parser('list', help='list expenses base on specific filters')
   parser_list.add_argument('type', help='the type of register to list', choices=['expense', 'income'])
   parser_list.add_argument('-all', help='list all expenses', action='store_true')
   parser_list.set_defaults(func=list_expenses)

def create_expense(args):
   validate_date(args.date)
   is_divided = 1 if args.div else 0
    
   con = sqlite3.connect('orme.db')
   cur = con.cursor()
   
   create_expenses_table_query = """
   CREATE TABLE if not exists expenses(
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      value INTEGER NOT NULL, 
      description TEXT, 
      is_divided INTEGER, 
      date DATE
      )
   """
   
   insert_into_expenses_query = f"""
   INSERT INTO expenses(
      value, 
      description, 
      is_divided, 
      date) VALUES(
         {args.val}, 
         '{args.desc}', 
         {is_divided}, 
         '{args.date}'
         )
   """
   
   cur.execute(create_expenses_table_query)
   cur.execute(insert_into_expenses_query) 

   con.commit()

   cur.close()
   con.close()
   
   print('The expense was registered successfully...')
    

def run_create_expense(subparser):
   parser_add = subparsers.add_parser('add', help='adds a new expense with all its attributes')
   parser_add.add_argument('type', help='the type of register to add', choices=['expense', 'income'])
   parser_add.add_argument('-val', type=int, help='The  of this particular expense (not the register)', required=True)
   parser_add.add_argument('-desc', type=str, help='The description of this particular expense', required=True)
   parser_add.add_argument('-date', type=str, help='Date of this particular expense (not the register date but the execute one) - default: current day', default=date.today().isoformat())
   parser_add.add_argument('-div', help='Whether this expense should be divided by 2 for calculation purposes', action='store_true')
   parser.set_defaults(func=create_expense)

if __name__ == '__main__':
   parser = argparse.ArgumentParser(
                     prog="Orme",
                     description="This program allows the user to register all its expenses",
                     epilog="TechSsus - Carlos Correa"   
                    )

   subparsers = parser.add_subparsers(title='[sub-commands]')
   run_create_expense(subparsers)
   run_list_expenses(subparsers)
   
   args = parser.parse_args()
   args.func(args)