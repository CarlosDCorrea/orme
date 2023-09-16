import argparse
import sqlite3
from datetime import date


def validate_date(str_date):
   try:
      date.fromisoformat(str_date)
   except ValueError as e:
      print(e)

def list_expenses(args):
   with sqlite3.connect('orme.db') as conn:
      cur = conn.cursor()
      list_expenses_query = """
      SELECT * FROM expenses
      """
      
      cur.execute(list_expenses_query)
      results = cur.fetchall()
      
      for row in results:
         print(row)
         
      cur.close()
         

def run_list_expenses(subparser):
   parser_list = subparsers.add_parser('list', help='list expenses base on specific filters')
   parser_list.add_argument('type', help='the type of register to list', choices=['expense', 'income'])
   parser_list.add_argument('-all', help='list all expenses', action='store_true')
   parser_list.set_defaults(func=list_expenses)

def create_expense(args):
   validate_date(args.date)
   today = date.today().isoformat()
   is_divided = 1 if args.div else 0
    
   con = sqlite3.connect('orme.db')
   cur = con.cursor()
   
   create_expenses_table_query = """
   CREATE TABLE if not exists expenses(
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      value INTEGER NOT NULL, 
      description TEXT, 
      is_divided INTEGER, 
      date TEXT,
      created TEXT,
      updated TEXT
      )
   """
   
   insert_into_expenses_query = f"""
   INSERT INTO expenses(
      value, 
      description, 
      is_divided, 
      date, created, updated) VALUES(
         {args.val}, 
         '{args.desc}', 
         {is_divided}, 
         '{args.date}',
         '{today}',
         '{today}'
         )
   """
   
   cur.execute(create_expenses_table_query)
   cur.execute(insert_into_expenses_query) 

   con.commit()

   cur.close()
   con.close()
   
   print('The expense was registered successfully...')

def run_create_expense(subparser):
   CATEGORIES = (
      'food', 
      'home',
      'bills',
      'technologic',
      'walk',
      'clothes'
   )
   
   REGISTER_TYPE = (
      'expense', 
      'income'
   )
   
   #TODO Try with a new register type user where dividing arguments in groups is neccesary
   parser_add = subparsers.add_parser('add', help='adds a new expense with all its attributes')
   parser_add.add_argument('type', help='the type of register to add', choices=REGISTER_TYPE)
   parser_add.add_argument('-val', type=int, help='The  of this particular expense (not the register)', required=True)
   parser_add.add_argument('-desc', type=str, help='The description of this particular expense', required=True)
   parser_add.add_argument('-caty', type=str, help='The category of the expense', choices=CATEGORIES)
   parser_add.add_argument('-date', type=str, help='Date of this particular expense (not the register date but the execute one) - default: current day', default=date.today().isoformat())
   parser_add.add_argument('-div', help='Whether this expense should be divided by 2 for calculation purposes', action='store_true')
   parser_add.set_defaults(func=create_expense)

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