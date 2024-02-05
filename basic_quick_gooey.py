#!/usr/bin/env python3
from enum import Enum
from pathlib import Path
from datetime import date, time

import gooey_quick


class UploadMethod(Enum):
    SFTP = 'SFTP'
    HTTP = 'HTTP'


def upload_file(
    file: Path,
    new_filename: str,
    chunksize: int,
    lattency: float,
    upload_date: date,
    upload_time: time,
    upload_method: UploadMethod,
):
    assert type(upload_method) is UploadMethod
    return (
        f'{file} was uploaded via {upload_method.name} on {upload_date} at '
        f'{upload_time} in chunks of size {chunksize} and with lattency of '
        f'{lattency}'
    )


if __name__ == '__main__':
    # gooey_quick.run_gooey has the same return values as the wrapped function
    return_value = gooey_quick.run_gooey(
        # the first argument is the fucntion you'd like to be converted into a Gooey program
        upload_file,
        # gooey_quick.run_gooey can be used to set Gooey's global configuration
        # see https://github.com/chriskiehl/Gooey#global-configuration for possible options
        program_name='Simple upload program',
        program_description='A demo program using Gooey and gooey_quick',
    )
    print(return_value)

