"""converters from Parameter into arg dict for gooey.GooeyParser.add_argument"""
from enum import Enum
from pathlib import Path
from datetime import date, time
from typing import Optional, Any, Union

from gooey_quick.introspection import Parameter
from gooey_quick.types import DirectoryPath, SaveToPath


def convert_to_argument(parameter: Parameter | Optional[Any]):
    """
    converts a parameter into dict of args for gooey.GooeyParser.add_argument

    :param parameter: parameter to be converted
    :raises ValueError: if parameter cannot be translated into a gooey widget
    :returns: dict of args to be passed int gooey.GooeyParser.add_argument
    """
    if parameter.is_optional and parameter.type_annotation is not bool:
        args = convert_to_argument(
                Parameter(
                    parameter.name,
                    type_annotation=parameter.type_annotation.__args__[0],
                    docstring=parameter.docstring,
                    default=parameter.default,
                )
        )
        args['required'] = False
        return args
    elif parameter.is_list and parameter.type_annotation.__args__[0] is Path:
        args = dict(
            action='store',
            type=Path,
            help=parameter.docstring,
            nargs='+',
            widget='MultiFileChooser',
        )
    elif parameter.type_annotation is DirectoryPath:
        args = dict(
            action='store',
            type=DirectoryPath,
            help=parameter.docstring,
            widget='DirChooser',
        )
    elif parameter.type_annotation is SaveToPath:
        args = dict(
            action='store',
            type=SaveToPath,
            help=parameter.docstring,
            widget='FileSaver',
        )
    elif parameter.type_annotation is Path:
        args = dict(
            type=Path,
            action='store',
            help=parameter.docstring,
            widget='FileChooser',
            gooey_options={
                'wildcard': "All files (*.*)|*.*",
            },
        )
    elif issubclass(parameter.type_annotation, Enum):
        args = dict(
            type=parameter.type_annotation.__getitem__,
            action='store',
            help=parameter.docstring,
            choices=list(parameter.type_annotation),
        )
    elif parameter.type_annotation is int:
        args = dict(
            type=int,
            action='store',
            help=parameter.docstring,
            widget='IntegerField',
        )
    elif parameter.type_annotation is float:
        args = dict(
            type=float,
            action='store',
            help=parameter.docstring,
            widget='DecimalField',
        )
    elif parameter.type_annotation is bool and parameter.has_default_value:
        args = dict(
            action='store_true',
            help=parameter.docstring,
            gooey_options={
                'initial_value': parameter.default,
            }
        )
    elif parameter.type_annotation is date:
        args = dict(
            action='store',
            help=parameter.docstring,
            type=date.fromisoformat,
            widget='DateChooser',
        )
    elif parameter.type_annotation is time:
        args = dict(
            action='store',
            help=parameter.docstring,
            type=time.fromisoformat,
            widget='TimeChooser',
        )
    elif parameter.type_annotation is str:
        args = dict(
            action='store',
            help=parameter.docstring,
            type=str,
        )
    else:
        raise ValueError(f'{parameter.type_annotation} cannot be translated into a Gooey widget!')

    args['dest'] = parameter.name
    args['metavar'] = parameter.name.capitalize().replace('_', ' ')
    args['required'] = not parameter.type_annotation is bool

    if parameter.has_default_value and parameter.type_annotation is not bool:
        args['default'] = parameter.default


    return args

