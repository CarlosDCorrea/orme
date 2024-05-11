import argparse
from datetime import date

from .expenses.run_expenses import create_expense, list_expenses
from orme import __app_name__, __version__
from .debt.run_debt import create_debt, list_debts


def run_create_expense(subparsers):
    CATEGORIES = (
        'food',
        'home',
        'bills',
        'technologic',
        'travel',
        'clothes',
        'other'
    )

    # This could be a tuple of users that can be get from the db
    USERS = (
        'Carlos',
        'Faby'
    )

    # TODO Try with a new register type user where dividing arguments in groups is neccesary
    parser_add = subparsers.add_parser('add',
                                       help='adds a new expense with all its attributes')

    parser_add.add_argument('-val',
                            '--value',
                            type=int,
                            help='The  of this particular expense (not the register)',
                            required=True)
    parser_add.add_argument('-desc',
                            '--description',
                            type=str,
                            help='The description of this particular expense',
                            required=True)
    parser_add.add_argument('-caty',
                            '--category',
                            type=str,
                            help='The category of the expense',
                            choices=CATEGORIES,
                            default=CATEGORIES[0])
    parser_add.add_argument('-u',
                            '--user',
                            type=str,
                            help='Name of the user that generate the expense',
                            choices=USERS,
                            default=USERS[0])
    parser_add.add_argument('-date',
                            type=str,
                            help="""
                            Date of this particular expense in isoformat YYYY-MM-DD
                            (not the register date but the execute one)
                            - default: current day""",
                            default=date.today().isoformat())
    parser_add.add_argument('-div',
                            help='Whether this expense should be divided by 2 for calculation purposes',
                            action='store_true')
    parser_add.set_defaults(func=create_expense)


def run_list_expenses(subparsers):
    parser_list = subparsers.add_parser('list',
                                        help='list expenses with filters')

    parser_list.add_argument('--gtd',
                             '-greater-than-date',
                             type=str,
                             help='Filter by dates greater than this one')
    parser_list.add_argument('--ltd',
                             '-less-than-date',
                             type=str,
                             help='Filter by dates less than this one')
    parser_list.add_argument('--date',
                             '-date',
                             type=str,
                             help='Filter by dates equal to this one')
    parser_list.add_argument('--gtv',
                             '-greater-than-value',
                             type=int,
                             help='Filter by values greater than this one')
    parser_list.add_argument('--ltv',
                             '-less-than-value',
                             type=int,
                             help='Filter by values less than this one')
    parser_list.add_argument('--value',
                             '-value',
                             type=int,
                             help='Filter by values equal to this one')
    parser_list.add_argument('--cat',
                             '-category',
                             type=str,
                             help='Filter by this specific category')
    parser_list.add_argument('--u',
                             '-user',
                             type=str,
                             help='Filter by the specified user')
    parser_list.set_defaults(func=list_expenses)


def run_create_dept(subparsers):
    parser_add = subparsers.add_parser('add',
                                       help='adds a new debt register whether the user is the debtor or the lender')
    parser_add.add_argument('-dp',
                            '--deptor',
                            type=str,
                            help='The name of the deptor [optional]'
                            )
    parser_add.add_argument('-ld',
                            '--lender',
                            type=str,
                            help='The name of the lender [optional]')
    parser_add.add_argument('-desc',
                            '--description',
                            type=str,
                            help='A short description of the dept [optional]')
    parser_add.add_argument('-val',
                            '--value',
                            type=str,
                            help='The value of the dept',
                            required=True)
    parser_add.add_argument('-ir',
                            '--interest-rate',
                            type=float,
                            help='The interest rate monthly of the dept default 0.0',
                            default=0.0)
    parser_add.add_argument('-date',
                            type=str,
                            help="""
                            Date of start of this particualr debt in isoformat YYYY-MM-DD
                            (not the register date but the execute one)
                            - default: current day""",
                            default=date.today().isoformat())
    parser_add.set_defaults(func=create_debt)


def run_list_depts(subparsers):
    parser_list = subparsers.add_parser('list',
                                        help='list depts with or without filteres')

    mutually_exclusive_by_value = parser_list.add_mutually_exclusive_group(required=True)
    mutually_exclusive_by_value.add_argument('--gtv',
                                             '-between-date',
                                             type=int,
                                             help='Filter by dates greater than this one')
    mutually_exclusive_by_value.add_argument('--ltv',
                                             '-between-value',
                                             type=int,
                                             help='Filter by values greater than this one')
    mutually_exclusive_by_value.add_argument('--eqv',
                                             '-equal-to-value',
                                             type=int,
                                             help='Filter by values equal to this one')
    mutually_exclusive_by_value.add_argument('--btv',
                                             '-between-values',
                                             type=int,
                                             help='Filter by values equal to this one',
                                             action='extend')
    mutually_exclusive_by_value.add_argument('--all',
                                             action='store_true')
    parser_list.set_defaults(func=list_debts)


def run_options(subparsers):
    parser_expenses = subparsers.add_parser('expenses',
                                            help='Executes all operations related to expenses')
    parser_debts = subparsers.add_parser('debts',
                                         help='Executes all operations related to debt')

    subparser_expenses = parser_expenses.add_subparsers(title='[sub-commands]')
    subparser_debts = parser_debts.add_subparsers(title='[sub-commands]')

    run_create_expense(subparser_expenses)
    run_list_expenses(subparser_expenses)

    run_create_dept(subparser_debts)
    run_list_depts(subparser_debts)


def main():
    parser = argparse.ArgumentParser(
        prog="Orme",
        description="""
                     This program allows the user to manage the expenses,
                     incomes and other financial situations
                     """,
        epilog="TechSsus - Carlos Correa"
    )

    # QUESTION: Support localization?
    parser.add_argument(
        '-v',
        '--version',
        help='Gives the version of the package',
        action='version',
        version=f'{__app_name__} version: {__version__}'
    )

    # REFACTOR: Commands should go 'expenses list' instead of 'list expenses'
    subparsers_options = parser.add_subparsers(title='[commands]')

    run_options(subparsers_options)

    args = parser.parse_args()
    print(f'These are the args: {args}')
    args.func(args)
