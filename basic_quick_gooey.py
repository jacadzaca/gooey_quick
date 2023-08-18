#!/usr/bin/env python3
import functools
from enum import Enum
from pathlib import Path
from datetime import date, time, datetime

from gooey import Gooey

import gooey_quick


class UploadMethod(Enum):
    SFTP = 'SFTP'
    HTTP = 'HTTP'

    def __str__(self):
        return self.name


def upload_file(
    file: Path,
    new_filename: str,
    chunksize: int,
    lattency: float,
    upload_date: date,
    upload_time: time,
    upload_method: UploadMethod,
):
    return (
        f'{file} was uploaded via {upload_method} on {upload_date} at '
        f'{upload_time} in chunks of size {chunksize} and with lattency of '
        f'{lattency}'
    )


@Gooey
def main():
    # gooey_quick.run_gooey has the same return values as the wrapped function
    print(gooey_quick.run_gooey(upload_file))


if __name__ == '__main__':
    main()

