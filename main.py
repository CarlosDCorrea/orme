import argparse
from datetime import date

from .expenses.run_expenses import create_expense, list_expenses

def run_list_expenses(subparser):
   parser_list = subparsers.add_parser('list', help='list expenses base on specific filters')
   parser_list.add_argument('type', help='the type of register to list', choices=['expense', 'income'])
   parser_list.add_argument('-all', help='list all expenses', action='store_true')
   parser_list.set_defaults(func=list_expenses)

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
   
   USERS = (
      'Carlos',
      'Faby'
   )
   
   #TODO Try with a new register type user where dividing arguments in groups is neccesary
   parser_add = subparsers.add_parser('add', help='adds a new expense with all its attributes')
   parser_add.add_argument('type', help='the type of register to add', choices=REGISTER_TYPE)
   parser_add.add_argument('-val', '--value', type=int, help='The  of this particular expense (not the register)', required=True)
   parser_add.add_argument('-desc', '--description', type=str, help='The description of this particular expense', required=True)
   parser_add.add_argument('-caty', '--category', type=str, help='The category of the expense', choices=CATEGORIES, default=CATEGORIES[0])
   parser_add.add_argument('-u', '--user', type=str, help='Name of the user that generate the expense', choices=USERS, default=USERS[0])
   parser_add.add_argument('-date', type=str, help='Date of this particular expense in isoformat YYYY-MM-DD (not the register date but the execute one) - default: current day', default=date.today().isoformat())
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