"""wrappers around Gooey that inspect callables"""
import inspect

from gooey import GooeyParser

from gooey_quick import converters


def create_parser(function: callable, parser: GooeyParser = None):
    """
    Crate a GooeyParser from a callabe

    :param function: callable to inspect for arguments
    :param parser: base parser
    :returns: a GooeyParser
    """
    if parser is None:
        parser = GooeyParser()

    for args in map(
        converters.convert_to_argument,
        inspect.signature(function).parameters.values()
    ):
        parameter_name = args['dest']
        if args.pop('required'):
            parser.add_argument(
                **args,
            )
        else:
            parser.add_argument(
                f'--{parameter_name}',
                **args,
            )

    return parser


def run_gooey(function: callable):
    argv = create_parser(function).parse_args()
    function(**argv.__dict__)
