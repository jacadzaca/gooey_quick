#!/usr/bin/env python3
from pathlib import Path

import gooey_quick


def copy_file(
    file: Path,
    new_filename: str,
    copy_count: int = 1,
):
    """
    We can use docstrings to set GooeyParser.add_argumet `help` attribute

    :param file: Filepath to copy from
    :param new_filename: Basis for the copied files' names'
    :param copy_count: How many copies to produce
    """
    for i in range(copy_count):
        print(f'Copying {file} as {new_filename}_{i + 1}...')


if __name__ == '__main__':
    gooey_quick.run_gooey(
        copy_file,
        program_name='Field from docstring example',
        program_description='Presents how to use docstrings to name your fields',
    )

