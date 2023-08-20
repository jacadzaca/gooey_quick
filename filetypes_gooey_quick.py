#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

import gooey_quick
from gooey_quick.types import DirectoryPath, SaveToPath


def copy_directory(
    copy_from: DirectoryPath,
    copy_to: DirectoryPath,
):
    return f'copying from {copy_from} to {copy_to}'


def rename_file(
    input_file: Path,
    output_file: SaveToPath,
):
    return f'renaming {input_file} to {output_file}'


def check_if_files_exist(
    files: list[Path],
):
    return '\n'.join((f'Does {file} exist? {file.exists()}' for file in files))


if __name__ == '__main__':
    print(
        gooey_quick.run_gooey({
            'Copy directory': copy_directory,
            'Rename file': rename_file,
            'Check for existance': check_if_files_exist,
        }),
    )

