from argparse import _SubParsersAction, ArgumentParser

from .run_user import (create_user,
                       list_users,
                       update_user,
                       delete_user)


def run_create_user_command(subparsers: _SubParsersAction):
    parser_add: ArgumentParser = subparsers.add_parser('add',
                                                       help='Adds a new user to reference in expenses and debts',
                                                       allow_abbrev=False)

    parser_add.add_argument('-fn',
                            '--first-name',
                            type=str,
                            help='The first name of the user (required)',
                            required=True)
    parser_add.add_argument('-ln',
                            '--last-name',
                            type=str,
                            help='The last name of the user (required)',
                            required=True)

    parser_add.set_defaults(func=create_user)


def run_list_users_command(subparsers: _SubParsersAction):
    parser_list: ArgumentParser = subparsers.add_parser('list',
                                                        help='List all the users in the system',
                                                        allow_abbrev=False)

    parser_list.set_defaults(func=list_users)


def run_update_user_command(subparsers: _SubParsersAction):
    parser_update: ArgumentParser = subparsers.add_parser('upddate',
                                                          help='Update the user with the specified id',
                                                          allow_abbrev=False)
    parser_update.add_argument('--id',
                               type=str,
                               help='The id of the user to be updated',
                               required=True)
    parser_update.add_argument('-fn',
                               '--first-name',
                               type=str,
                               help='The new first name of the user')
    parser_update.add_argument('-ln',
                               '--last-name',
                               type=str,
                               help='The new last name of the user')

    parser_update.set_defaults(func=update_user)


def run_delete_user_command(subparsers: _SubParsersAction):
    parser_delete: ArgumentParser = subparsers.add_parser('delete',
                                                          help='Delete the user witht he specified id')

    parser_delete.add_argument('--id',
                               type=str,
                               help='The id of the user to be deleted',
                               required=True)

    parser_delete.set_defaults(func=delete_user)
