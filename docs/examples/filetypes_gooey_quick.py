#!/usr/bin/env python3
from pathlib import Path
from typing import Optional, Literal

import gooey_quick
from gooey_quick.types import DirectoryPath, SaveToPath, FileWithExtension


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


def preveiw_json(
    json_file: FileWithExtension[Literal['json']],
):
    return f'Preview of {json_file} is ...'


def convert_files_to_jsons(
    files_to_convert: list[FileWithExtension[Literal['csv', 'xml']]],
):
    return '\n'.join((f'Converting {file} to {file.stem}.json...' for file in files_to_convert))


if __name__ == '__main__':
    print(
        gooey_quick.run_gooey(
        {
            'Copy directory': copy_directory,
            'Rename file': rename_file,
            'Check for existance': check_if_files_exist,
            'Convert CSV to JSON': convert_files_to_jsons,
            'Preview JSON': preveiw_json,
        },
        program_name='A file wrangling program',
        program_description="A demo program using Gooey and gooey_quick filetypes",
      ),
    )

