import argparse
from argparse import ArgumentParser, _SubParsersAction

from orme import __app_name__, __version__

from .debt.commands import (run_create_debt_command,
                            run_list_debts_command,
                            run_update_debt_command,
                            run_delete_debt_command,
                            run_get_debt_command)

from .expense.commands import (run_create_expense_command,
                               run_list_expenses_command,
                               run_update_expenses_command,
                               run_delete_expense_command,
                               run_total_command)


def run_options(subparsers: _SubParsersAction) -> None:
    parser_expenses: ArgumentParser = subparsers.add_parser('expenses',
                                                            help='Executes all operations related to expenses')
    parser_debts: ArgumentParser = subparsers.add_parser('debts',
                                                         help='Executes all operations related to debt')

    subparser_expenses: _SubParsersAction[ArgumentParser] = parser_expenses.add_subparsers(
        title='[sub-commands]')
    subparser_debts:  _SubParsersAction[ArgumentParser] = parser_debts.add_subparsers(
        title='[sub-commands]')

    run_create_expense_command(subparser_expenses)
    run_list_expenses_command(subparser_expenses)
    run_update_expenses_command(subparser_expenses)
    run_delete_expense_command(subparser_expenses)
    run_total_command(subparser_expenses)

    run_create_debt_command(subparser_debts)
    run_list_debts_command(subparser_debts)
    run_update_debt_command(subparser_debts)
    run_delete_debt_command(subparser_debts)
    run_get_debt_command(subparser_debts)


def main():
    parser: ArgumentParser = argparse.ArgumentParser(
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

    subparsers_options: _SubParsersAction[ArgumentParser] = parser.add_subparsers(
        title='[commands]')

    run_options(subparsers_options)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except Exception as e:
            print(e)
    else:
        parser.parse_args(['--h'])
