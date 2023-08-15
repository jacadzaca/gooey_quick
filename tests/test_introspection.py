from typing import Optional
from inspect import Parameter

import pytest

from gooey_quick.introspection import Parameter as ParameterTested


def some_function(foo: str, bar: int, foobar: float):
    """This function does something
        :param foo: an argument
        :param bar: another argument
        :param foobar: yet another argument
        :returns: None
    """
    pass


@pytest.mark.parametrize('function, expected_parameters', [
    (
        some_function,
        [
            ParameterTested(name='foo', type_annotation=str, docstring='an argument'),
            ParameterTested(name='bar', type_annotation=int, docstring='another argument'),
            ParameterTested(name='foobar', type_annotation=float, default=1.2, docstring='yet another argument'),
        ],
    ),
])
def test_parse_callable_parameters_parses_properly(function, expected_parameters):
    def mock_function_inspector(function):
        if function == some_function:
            return [
                Parameter(
                    'foo',
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=str,
                ),
                Parameter(
                    'bar',
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=int,
                ),
                Parameter(
                    'foobar',
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=float,
                    default=1.2,
                ),
            ]
        else:
            raise ValueError(f'cannot mock function {functions}')

    assert ParameterTested.parse_callable_parameters(
        function,
        signature_extractor=mock_function_inspector,
    ) == expected_parameters


@pytest.mark.parametrize('type_annotation, expected_is_optional', [
    (str, False),
    (int, False),
    (float, False),
    (bool, True),
    (Optional[str], True),
    (Optional[float], True),
    (Optional[int], True),
])
def test_parse_callable_parameters_parses_optionals_properly(type_annotation, expected_is_optional):
    if type_annotation is bool:
        assert ParameterTested('some_name', type_annotation, 'some docstring', default=True).is_optional == expected_is_optional
    else:
        assert ParameterTested('some_name', type_annotation, 'some docstring').is_optional == expected_is_optional


@pytest.mark.parametrize('name, type_annotation, default', [
    (
        'bool_field_no_default',
        bool,
        Parameter.empty,
    ),
    (
        'optional_field_more_than_one_types',
        Optional[str | int],
        Parameter.empty,
    ),
    (
        'optional_field_more_than_one_types',
        Optional[str | int | float],
        Parameter.empty,
    ),
    (
        'optional_field_with_default_non_null_value',
        Optional[str | int],
        'test',
    ),
])
def test_invalid_parameters_dont_parse(name, type_annotation, default):
    with pytest.raises(ValueError):
        ParameterTested(name, type_annotation, 'some docstring', default=default)

