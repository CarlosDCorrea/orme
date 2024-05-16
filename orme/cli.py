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
                                       help='adds a new expense with all its attributes',
                                       allow_abbrev=False)

    parser_add.add_argument('-v',
                            '--value',
                            type=int,
                            help='The  of this particular expense (not the register)',
                            required=True)
    parser_add.add_argument('-desc',
                            '--description',
                            type=str,
                            help='The description of this particular expense [optional]')
    # For future versions categories and users should be data from the database
    parser_add.add_argument('-caty',
                            '--category',
                            type=str,
                            help='The category of the expense (default: food)',
                            choices=CATEGORIES,
                            default=CATEGORIES[0])
    parser_add.add_argument('-u',
                            '--user',
                            type=str,
                            help='Name of the user that generate the expense (default: Carlos)',
                            choices=USERS,
                            default=USERS[0])
    parser_add.add_argument('--date',
                            type=str,
                            help="""
                            The date when this expense ocurred in isoformat YYYY-MM-DD
                            (not the register date but the execute one)
                            - default: current day""",
                            default=date.today().isoformat())
    parser_add.add_argument('--div',
                            help='Whether this expense should be divided by 2 for calculation purposes',
                            action='store_true')

    parser_add.set_defaults(func=create_expense)


def run_list_expenses(subparsers):
    parser_list = subparsers.add_parser('list',
                                        help='list expenses with filters',
                                        allow_abbrev=True)

    mutually_exclusive_by_value = parser_list.add_mutually_exclusive_group()
    mutually_exclusive_by_date = parser_list.add_mutually_exclusive_group()

    # In the future could be only a query command that is able to resolve every query db
    mutually_exclusive_by_value.add_argument('-gtv',
                                             '--greater-than-value',
                                             type=int,
                                             help='Filter by values greater than this one')
    mutually_exclusive_by_value.add_argument('-ltv',
                                             '--less-than-value',
                                             type=int,
                                             help='Filter by values less than this one')
    mutually_exclusive_by_value.add_argument('-btv',
                                             '--between-value',
                                             nargs=2,
                                             type=int,
                                             metavar=('start-value',
                                                      'end-value'),
                                             action='extend',
                                             help='Filter by the values provided (inclusive)')
    mutually_exclusive_by_value.add_argument('-eqv',
                                             '--equal-to-value',
                                             type=int,
                                             help="Filter by values equals to this one")
    mutually_exclusive_by_date.add_argument('-gtd',
                                            '--greater-than-date',
                                            type=str,
                                            help='Filter by dates greater than this one')
    mutually_exclusive_by_date.add_argument('-ltd',
                                            '--less-than-date',
                                            type=str,
                                            help='Filter by dates less than this one')
    mutually_exclusive_by_date.add_argument('-btd',
                                            '--between-date',
                                            nargs=2,
                                            type=int,
                                            metavar=('start-date', 'end-date'),
                                            action='extend',
                                            help='Filter by the dates provided (inclusive)')
    mutually_exclusive_by_date.add_argument('-eqd',
                                            '--equal-to-date',
                                            type=int,
                                            help="Filter by dates equals to this one")
    parser_list.add_argument('-caty',
                             '--category',
                             type=str,
                             help='Filter by this specific category')
    parser_list.add_argument('-u',
                             '--user',
                             type=str,
                             help='Filter by the specified user')
    parser_list.set_defaults(func=list_expenses)


def run_create_dept(subparsers):
    parser_add = subparsers.add_parser('add',
                                       help='adds a new debt register whether the user is the debtor or the lender',
                                       allow_abbrev=False)
    # TODO: Read more about the names of the arguments (dest, metavar)
    parser_add.add_argument('-v',
                            '--value',
                            type=int,
                            help='The value of the dept',
                            required=True)
    parser_add.add_argument('-dpr',
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
    parser_add.add_argument('-ir',
                            '--interest-rate',
                            type=float,
                            help='The interest rate monthly of the dept default 0.0',
                            default=0.0)
    parser_add.add_argument('--date',
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

    mutually_exclusive_by_value = parser_list.add_mutually_exclusive_group()
    mutually_exclusive_by_date = parser_list.add_mutually_exclusive_group()

    mutually_exclusive_by_value.add_argument('-gtv',
                                             '--greater-than-value',
                                             type=int,
                                             help='Filter by values greater than this one (inclusive)')
    mutually_exclusive_by_value.add_argument('-ltv',
                                             '--lower-than-value',
                                             type=int,
                                             help='Filter by values lower than this one (inclusive)')
    mutually_exclusive_by_value.add_argument('-eqv',
                                             '--equal-to-value',
                                             type=int,
                                             help='Filter by values equal to this one')
    mutually_exclusive_by_value.add_argument('-btv',
                                             '--between-values',
                                             nargs=2,
                                             metavar=('value-start',
                                                      'value-end'),
                                             type=int,
                                             help='Filter by values between the values provided (inclusive)',
                                             action='extend')
    mutually_exclusive_by_date.add_argument('-gtd',
                                            '--greater-than-date',
                                            type=str,
                                            help='Filter by dates greater than this one (inclusive)')
    mutually_exclusive_by_date.add_argument('-ltd',
                                            '--lower-than-date',
                                            type=str,
                                            help='Filter by dates lower than this one (inclusive)')
    mutually_exclusive_by_date.add_argument('-eqd',
                                            '--equal-to-date',
                                            type=str,
                                            help='Filter by dates equal to this one')
    mutually_exclusive_by_date.add_argument('-btd',
                                            '--between-dates',
                                            nargs=2,
                                            metavar=('date-start', 'date-end'),
                                            type=str,
                                            help='Filter by dates between the dates provided (inclusive)',
                                            action='extend')

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
