import argparse
from datetime import date

from .expenses.run_expenses import create_expense, list_expenses
from orme import __app_name__, __version__
from .dept.run_dept import create_dept


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
    """ value_exclusive_group.add_argument('--gt',
                                       '-greater-than',
                                       action='store_true',
                                       help='Filter by values greater than this')
    value_exclusive_group.add_argument('--lt',
                                       '-less-than',
                                       action='store_true',
                                       help='Filter by values less than this')
    value_exclusive_group.add_argument('--eq',
                                       '-equal',
                                       action='store_true',
                                       help='Filter by values equal to this') """
    """ parser_list.add_argument('type',
                             help='the type of register to list',
                             choices=['expense', 'income']) """
    parser_list.set_defaults(func=list_expenses)


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

    REGISTER_TYPE = (
        'expense',
        'income'
    )

    # This could be a tuple of users that can be get from the db
    USERS = (
        'Carlos',
        'Faby'
    )

    # TODO Try with a new register type user where dividing arguments in groups is neccesary
    parser_add = subparsers.add_parser('add',
                                       help='adds a new expense with all its attributes')
    parser_add.add_argument('type',
                            help='the type of register to add',
                            choices=REGISTER_TYPE)
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
                            action='store_const',
                            const=0.0)
    parser_add.set_defaults(func=create_dept)


def run_list_depts(subparsers):
    parser_list = subparsers.add_parser('list',
                                        help='list depts with or without filteres')

    parser_list.add_argument('--btd',
                             '-between-date',
                             type=str,
                             help='Filter by dates greater than this one',
                             action='extend')
    parser_list.add_argument('--date',
                             '-date',
                             type=str,
                             help='Filter by dates equal to this one')
    parser_list.add_argument('--btv',
                             '-between-value',
                             type=int,
                             help='Filter by values greater than this one')
    parser_list.add_argument('--value',
                             '-value',
                             type=int,
                             help='Filter by values equal to this one')


def package_info(args):
    if args.version:
        print(f'{__app_name__} version: {__version__}')


def main():
    parser = argparse.ArgumentParser(
        prog="Orme",
        description="""
                     This program allows the user to manage the expenses,
                     incomes and other financial situations
                     """,
        epilog="TechSsus - Carlos Correa"
    )

    parser.add_argument(
        '-v',
        '--version',
        help='Gives the version of the package',
        action='version',
        version='%(prog)s 1.0'
    )

    parser.set_defaults(func=package_info)

    subparsers = parser.add_subparsers(title='[sub-commands]')
    run_create_expense(subparsers)
    run_list_expenses(subparsers)

    run_create_dept(subparsers)
    run_list_depts(subparsers)

    args = parser.parse_args()
    args.func(args)
