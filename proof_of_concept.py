#!/usr/bin/env python3
import inspect
import pathlib
import enum
from datetime import date, time, datetime
from inspect import Parameter
from pathlib import Path
from enum import Enum
from argparse import Action

from gooey import Gooey, GooeyParser

class NetworkConnection:
    def connect():
        print('connecting to network')


class Database:
    def connect():
        print('connecting to database')


class Connection(Enum):
    Network = NetworkConnection
    Database = Database

    def __str__(self):
        return self.name


def upload_json(file: Path, database_connection: Connection, chunksize: int, some_float: float, upload_date: date, upload_time: time, test: str, send_as_csv: bool = False):
    print(f'{file} {database_connection} {chunksize} {send_as_csv}')


def create_parser(parameters, use_gooey_widgets=True):
    parser = GooeyParser(prog='example_program')
    for parameter in parameters:
        if parameter.annotation is Path:
            parser.add_argument(
                parameter.name,
                type=Path,
                widget='FileChooser',
                default=parameter.default if parameter.default is not Parameter.empty else None,
                gooey_options={
                    'wildcard': "All files (*.*)|*.*",
                },
            )
        elif issubclass(parameter.annotation, Enum):
            parser.add_argument(
                parameter.name,
                type=parameter.annotation.__getitem__,
                action='store',
                default=parameter.default if parameter.default is not Parameter.empty else None,
                choices=list(parameter.annotation),
            )
        elif parameter.annotation is int:
            parser.add_argument(
                parameter.name,
                type=int,
                action='store',
                default=parameter.default if parameter.default is not Parameter.empty else None,
                widget='IntegerField' if use_gooey_widgets else None,
            )
        elif parameter.annotation is float:
            parser.add_argument(
                parameter.name,
                type=float,
                action='store',
                default=parameter.default if parameter.default is not Parameter.empty else None,
                widget='DecimalField' if use_gooey_widgets else None,
            )
        elif parameter.annotation is bool:
            has_default_values = parameter.default is not Parameter.empty
            parser.add_argument(
                f'--{parameter.name}' if has_default_values else parameter.name,
                action='store_true',
                default=parameter.default if has_default_values else None,
            )
        elif parameter.annotation is date:
            parser.add_argument(
                parameter.name,
                action='store',
                type=date.fromisoformat,
                widget='DateChooser',
            )
        elif parameter.annotation is time:
            parser.add_argument(
                dest=parameter.name,
                action='store',
                type=time.fromisoformat,
                widget='TimeChooser',
            )
        elif parameter.annotation is str:
            parser.add_argument(
                parameter.name,
                action='store',
                type=str,
            )
        else:
            raise ValueError(f'{parameter.annotation} cannot be translated into a Gooey widget!')
    return parser


@Gooey(
    language='polish',
)
def main(parser):
    argv = parser.parse_args()
    print(argv)
    print(type(argv.database_connection))
    argv.database_connection.value.connect()
    upload_json(**argv.__dict__)



if __name__ == '__main__':
    #upload_json(Path('some_json.json'), Connection.Network, 10**6)
    #upload_json(Path('some_json.json'), Connection.Network, 10**6, send_as_csv=True)

    signature = inspect.signature(upload_json)
    parser = create_parser(signature.parameters.values(), use_gooey_widgets=False)
    main(parser)

