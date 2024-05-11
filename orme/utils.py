import types
from argparse import Namespace
from typing import List, Tuple, Union


def get_present_arguments(args: Namespace) -> List[Tuple[str, Union[str, int]]]:
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    return present_arguments


def get_operator(args: List[Tuple[str, Union[str, int]]]) -> str | None:
    print(args)
    match args:
        case [(arg, _)] if arg.startswith('bt'):
            return 'bt'
        case [(arg, _)] if arg.startswith('gt'):
            return 'gt'
        case [(arg, _)] if arg.startswith('lt'):
            return 'lt'
        case [(arg, _)] if arg.startswith('eq'):
            return '='
        case _:
            return None
