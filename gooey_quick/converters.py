"""converters from inspect.Parameter into arg dict for gooey.GooeyParser.add_argument"""
from enum import Enum
from pathlib import Path
from inspect import Parameter
from datetime import date, time
from typing import Optional, Any, Union


def convert_to_argument(parameter: Parameter | Optional[Any]):
    """
    converts a parameter (usually acqiured from a function signature)
    into dict of args for gooey.GooeyParser.add_argument

    :param parameter: parameter to be converted
    :raises ValueError: if parameter cannot be translated into a gooey widget
    :returns: dict of args to be passed int gooey.GooeyParser.add_argument
    """
    parameter_has_default_value = parameter.default is not Parameter.empty
    parameter_is_optional = hasattr(parameter.annotation, '__origin__') and parameter.annotation.__origin__ is Union

    if parameter_is_optional:
        optional_annotation = parameter.annotation.__args__[0]

        if len(parameter.annotation.__args__) != 2:
            raise ValueError(f'quick_gooey dose not support Optional fields with many possible type values')
        elif optional_annotation is bool:
            raise ValueError('bool arguments are optional by default')
        elif parameter_has_default_value and parameter.default is not None:
            raise ValueError(f'Optionals with default non None values are inappropriate see https://docs.python.org/3/library/typing.html#typing.Optional')
        args = convert_to_argument(
                Parameter(
                    parameter.name,
                    parameter.kind,
                    annotation=optional_annotation,
                    default=parameter.default,
                )
        )
        args['required'] = False
        return args
    elif parameter.annotation is Path:
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
            action='store_true',
            gooey_options={
                'initial_value': parameter.default,
            }
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
    args['required'] = not parameter.annotation is bool

    if parameter_has_default_value and parameter.annotation is not bool:
        args['default'] = parameter.default


    return args

