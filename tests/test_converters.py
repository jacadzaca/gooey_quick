from enum import Enum
from pathlib import Path
from typing import Optional
from inspect import Parameter
from datetime import date, time

import pytest

from gooey_quick import converters


class ExampleEnum(Enum):
    ONE = 1
    TWO = 2

    def __str__(self):
        return self.name


test_parameter_is_properly_converted_cases = [
    (
        Parameter(
            'file',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Path,
        ),
        dict(
            dest='file',
            action='store',
            type=Path,
            widget='FileChooser',
            gooey_options=dict(wildcard='All files (*.*)|*.*'),
            required=True,
        ),
        'functions with a Path argument are properly converted',
    ),
    (
        Parameter(
            'file',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Path,
            default=Path('home/'),
        ),
        dict(
            dest='file',
            action='store',
            type=Path,
            widget='FileChooser',
            gooey_options=dict(wildcard='All files (*.*)|*.*'),
            default=Path('home/'),
            required=True,
        ),
        'functions with a Path argument and a default value are properly converted',
    ),
    (
        Parameter(
            'choice_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=ExampleEnum,
        ),
        dict(
            dest='choice_field',
            action='store',
            type=ExampleEnum.__getitem__,
            choices=list(ExampleEnum),
            required=True,
        ),
        'functions with an Enum argument are properly converted',
    ),
    (
        Parameter(
            'choice_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=ExampleEnum,
            default=ExampleEnum.ONE,
        ),
        dict(
            dest='choice_field',
            action='store',
            type=ExampleEnum.__getitem__,
            choices=list(ExampleEnum),
            default=ExampleEnum.ONE,
            required=True,
        ),
        'functions with an Enum argument and a default value are properly converted',
    ),
    (
        Parameter(
            'int_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=int,
        ),
        dict(
            dest='int_field',
            action='store',
            type=int,
            widget='IntegerField',
            required=True,
        ),
        'functions with an int argument are properly converted',
    ),
    (
        Parameter(
            'int_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=int,
            default=1,
        ),
        dict(
            dest='int_field',
            action='store',
            type=int,
            default=1,
            widget='IntegerField',
            required=True,
        ),
        'functions with an int argument and a default value are properly converted',
    ),
    (
        Parameter(
            'float_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=float,
        ),
        dict(
            dest='float_field',
            action='store',
            type=float,
            widget='DecimalField',
            required=True,
        ),
        'functions with an float argument are properly converted',
    ),
    (
        Parameter(
            'float_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=float,
            default=1.2,
        ),
        dict(
            dest='float_field',
            action='store',
            type=float,
            default=1.2,
            widget='DecimalField',
            required=True,
        ),
        'functions with an float argument and a default value are properly converted',
    ),
    (
        Parameter(
            'bool_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=bool,
            default=True,
        ),
        dict(
            dest='bool_field',
            action='store_false',
            required=False,
        ),
        'functions with an bool argument and a default True value are properly converted',
    ),
    (
        Parameter(
            'bool_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=bool,
            default=False,
        ),
        dict(
            dest='bool_field',
            action='store_true',
            required=False,
        ),
        'functions with an bool argument and a default False value are properly converted',
    ),
    (
        Parameter(
            'date_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=date,
        ),
        dict(
            dest='date_field',
            action='store',
            type=date.fromisoformat,
            widget='DateChooser',
            required=True,
        ),
        'functions with an date argument are properly converted',
    ),
    (
        Parameter(
            'date_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=date,
            default=date(year=2002, month=7, day=22),
        ),
        dict(
            dest='date_field',
            action='store',
            type=date.fromisoformat,
            default=date(year=2002, month=7, day=22),
            widget='DateChooser',
            required=True,
        ),
        'functions with an date argument and a default value are properly converted',
    ),
    (
        Parameter(
            'time_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=time,
        ),
        dict(
            dest='time_field',
            action='store',
            type=time.fromisoformat,
            widget='TimeChooser',
            required=True,
        ),
        'functions with an time argument are properly converted',
    ),
    (
        Parameter(
            'time_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=time,
            default=time(hour=21, minute=37, second=10),
        ),
        dict(
            dest='time_field',
            action='store',
            type=time.fromisoformat,
            default=time(hour=21, minute=37, second=10),
            widget='TimeChooser',
            required=True,
        ),
        'functions with an time argument and a default value are properly converted',
    ),
    (
        Parameter(
            'string_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=str,
        ),
        dict(
            dest='string_field',
            action='store',
            type=str,
            required=True,
        ),
        'functions with an string argument are properly converted',
    ),
    (
        Parameter(
            'string_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=str,
            default='test',
        ),
        dict(
            dest='string_field',
            action='store',
            type=str,
            default='test',
            required=True,
        ),
        'functions with an string argument and a default value are properly converted',
    ),
    (
        Parameter(
            'optional_field',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Optional[str],
        ),
        dict(
            dest='optional_field',
            action='store',
            type=str,
            required=False,
        ),
        'functions with an Optional argument are properly converted',
    ),
    (
        Parameter(
            'optional_field_with_none_default',
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Optional[str],
            default=None,
        ),
        dict(
            dest='optional_field_with_none_default',
            action='store',
            type=str,
            required=False,
            default=None,
        ),
        'functions with an Optional argument and None default value are properly converted',
    ),
]


@pytest.mark.parametrize(
    argnames=('parameter', 'expected_add_argument_args'),
    argvalues=(case[0:2] for case in test_parameter_is_properly_converted_cases),
    ids=[case[2] for case in test_parameter_is_properly_converted_cases],
)
def test_parameter_is_properly_converted(parameter, expected_add_argument_args):
    assert converters.convert_to_argument(parameter) == expected_add_argument_args


@pytest.mark.parametrize('untranslatable_parameter', [
    Parameter(
        'composite_field',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=dict,
        default=dict(x=1),
    ),
    Parameter(
        'composite_optional_field',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[dict],
    ),
    Parameter(
        'bool_field_no_default',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=bool,
    ),
    Parameter(
        'optional_field_more_than_one_types',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[str | int],
    ),
    Parameter(
        'optional_field_more_than_one_types',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[str | int | float],
    ),
    Parameter(
        'optional_field_with_default_non_null_value',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[str | int],
        default='test',
    ),
    Parameter(
        'optional_bool_field',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[bool],
    ),
    Parameter(
        'optional_bool_field_with_non_none_default',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[bool],
        default=True,
    ),
    Parameter(
        'optional_bool_field_with_none_default',
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Optional[bool],
        default=None,
    ),
])
def test_parameter_conversion_raises_value_error_if_cant_translate_parameter(untranslatable_parameter):
    with pytest.raises(ValueError):
        converters.convert_to_argument(untranslatable_parameter)

