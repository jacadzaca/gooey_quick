"""converters from inspect.Parameter into arg dict for gooey.GooeyParser.add_argument"""
from enum import Enum
from pathlib import Path
from inspect import Parameter
from datetime import date, time


def convert_to_argument(parameter: Parameter):
    """
    converts a parameter (usually acqiured from a function signature)
    into dict of args for gooey.GooeyParser.add_argument

    :param parameter: parameter to be converted
    :raises ValueError: if parameter cannot be translated into a gooey widget
    :returns: dict of args to be passed int gooey.GooeyParser.add_argument
    """
    parameter_has_default_value = parameter.default is not Parameter.empty

    if parameter.annotation is Path:
        args = dict(
            type=Path,
            action='store',
            widget='FileChooser',
            gooey_options={
                'wildcard': "All files (*.*)|*.*",
            },
        )
    elif issubclass(parameter.annotation, Enum):
        args = dict(
            type=parameter.annotation.__getitem__,
            action='store',
            choices=list(parameter.annotation),
        )
    elif parameter.annotation is int:
        args = dict(
            type=int,
            action='store',
            widget='IntegerField',
        )
    elif parameter.annotation is float:
        args = dict(
            type=float,
            action='store',
            widget='DecimalField',
        )
    elif parameter.annotation is bool and parameter_has_default_value:
        args = dict(
            action='store_false' if parameter.default else 'store_true',
        )
    elif parameter.annotation is date:
        args = dict(
            action='store',
            type=date.fromisoformat,
            widget='DateChooser',
        )
    elif parameter.annotation is time:
        args = dict(
            action='store',
            type=time.fromisoformat,
            widget='TimeChooser',
        )
    elif parameter.annotation is str:
        args = dict(
            action='store',
            type=str,
        )
    else:
        raise ValueError(f'{parameter.annotation} cannot be translated into a Gooey widget!')

    args['dest'] = parameter.name

    if parameter_has_default_value and parameter.annotation is not bool:
        args['default'] = parameter.default

    return args

