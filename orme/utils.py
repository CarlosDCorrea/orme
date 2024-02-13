import types
from argparse import Namespace
from typing import List, Tuple


def get_present_arguments(args: Namespace) -> List[Tuple]:
    present_arguments = [
        (argument, value) for argument, value in vars(args).items()
        if value is not None and not isinstance(value, types.FunctionType)
    ]

    return present_arguments
