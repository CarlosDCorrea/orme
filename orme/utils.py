import types
from argparse import Namespace
from typing import List, Tuple, Dict


def get_present_arguments(args: Namespace) -> List[Tuple[str, str | int]]:
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    return present_arguments


def get_dict_present_arguments(args: Namespace) -> Dict[str, str | int]:
    present_arguments = {field: value for field, value in vars(args).items()
                         if value is not None and not isinstance(value, types.FunctionType)}

    return present_arguments
