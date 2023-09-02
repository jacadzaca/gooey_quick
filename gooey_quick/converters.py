"""converters from Parameter into arg dict for gooey.GooeyParser.add_argument"""
from enum import Enum
from pathlib import Path
from datetime import date, time
from typing import Optional, Any, Union

from gooey_quick.introspection import Parameter
from gooey_quick.types import DirectoryPath, SaveToPath, FileWithExtension


def convert_optional(parameter: Parameter) -> dict[str, Any]:
    return {
        **DEFAULT_TYPE_INTERPRETATION[parameter.type_annotation],
        'required': False,
    }


def convert_file_with_extension(parameter: Parameter) -> dict[str, Any]:
    allowed_file_types = '|'.join((f'{filetype.upper()} (*.{filetype})|*.{filetype}' for filetype in parameter.args))
    allowed_file_types += '|All files (*.*)|*.*'
    return {
        'type': FileWithExtension,
        'widget': 'FileChooser',
        'gooey_options': {
            'wildcard': allowed_file_types,
        },
    }


def convert_list(parameter: Parameter) -> dict[str, Any]:
    if parameter.type_annotation is Path:
        return {
            'type': Path,
            'nargs': '+',
            'widget': 'MultiFileChooser',
        }
    elif parameter.origin is FileWithExtension:
        return {
            **convert_file_with_extension(
                Parameter(
                    parameter.name,
                    parameter.args,
                    parameter.docstring,
                    parameter.default,
                )
            ),
            'widget': 'MultiFileChooser',
            'nargs': '+',
        }
    else:
        raise ValueError(f'list of {parameter.type_annotation} cannot be translated into a Gooey widget!')


def convert_enum(parameter: Parameter) -> dict[str, Any]:
    return {
        'type': parameter.type_annotation.__getitem__,
        'choices': list(parameter.type_annotation),
    }


DEFAULT_ORIGIN_CONVERTERS = {
    list:               convert_list,
    Optional:           convert_optional,
    FileWithExtension:  convert_file_with_extension
}


DEFAULT_TYPE_INTERPRETATION = {
    str: {
        'type': str,
    },
    int: {
        'type': int,
        'widget': 'IntegerField',
    },
    bool: {
        'action': 'store_true',
        'required': False,
    },
    float: {
        'type': float,
        'widget': 'DecimalField',
    },
    date: {
        'type': date.fromisoformat,
        'widget': 'DateChooser',
    },
    time: {
        'type': time.fromisoformat,
        'widget': 'TimeChooser',
    },
    Path: {
        'type': Path,
        'widget': 'FileChooser',
        'gooey_options': {
            'wildcard': "All files (*.*)|*.*",
        },
    },
    SaveToPath: {
        'type': SaveToPath,
        'widget': 'FileSaver',
    },
    DirectoryPath: {
        'type': DirectoryPath,
        'widget': 'DirChooser',
    },
}


DEFAULT_SUBTYPES_CONVERTERS = {
    Enum: convert_enum,
}


def convert_to_argument(parameter: Parameter | Optional[Any]):
    """
    converts a parameter into dict of args for gooey.GooeyParser.add_argument

    :param parameter: parameter to be converted
    :raises ValueError: if parameter cannot be translated into a gooey widget
    :returns: dict of args to be passed int gooey.GooeyParser.add_argument
    """

    args = {
        'dest': parameter.name,
        'metavar': parameter.name.capitalize().replace('_', ' '),
        'required': True,
        'action': 'store',
        'help': parameter.docstring,
    }

    if parameter.type_annotation is bool:
        args['gooey_options'] = {
            'initial_value': parameter.default,
        }

    if parameter.has_default_value and parameter.type_annotation is not bool:
        args['default'] = parameter.default

    try:
        if parameter.origin in DEFAULT_ORIGIN_CONVERTERS:
            convert = DEFAULT_ORIGIN_CONVERTERS[parameter.origin]
            type_specific_args = convert(
                Parameter(
                    parameter.name,
                    parameter.args,
                    docstring=parameter.docstring,
                    default=parameter.default,
                )
            )
        elif parameter.type_annotation in DEFAULT_TYPE_INTERPRETATION:
            type_specific_args = DEFAULT_TYPE_INTERPRETATION[parameter.type_annotation]
        else:
            for parent_type in DEFAULT_SUBTYPES_CONVERTERS:
                if issubclass(parameter.type_annotation, parent_type):
                    convert = DEFAULT_SUBTYPES_CONVERTERS[parent_type]
                    type_specific_args = convert(parameter)
                    break
            else:
                raise KeyError()
    except KeyError:
        raise ValueError(f'{parameter.type_annotation} cannot be translated into a Gooey widget!')


    return {**args, **type_specific_args}

