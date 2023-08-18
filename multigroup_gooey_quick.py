#!/usr/bin/env python3
from pathlib import Path
from typing import Optional
from datetime import date, datetime

from gooey import Gooey, GooeyParser

import gooey_quick


def search_history(
    history_file: Path,
    wanted_phrase: str,
    min_occure_date: Optional[date] = None,
    max_occure_date: Optional[date] = None,
) -> Optional[tuple[date, str]]:
    occurance_date = date(year=2002, month=7, day=22)
    the_phrase = "wow you have discovered my secret phrase!"
    occurance_in_range = True

    if min_occure_date is not None and max_occure_date is not None:
        print(f'Looking for {wanted_phrase} from {min_occure_date} to {max_occure_date}...')
        occurance_in_range = occurance_date in range(min_occure_date, max_occure_date)

    if wanted_phrase in the_phrase and occurance_in_range:
        print(f'{occurance_date}: {the_phrase}')


def append_to_history(
    history_file: Path,
    phrase: str,
    occurance_date: date = datetime.now().date()
):
    print(f'Appending {phrase} to {history_file} at {occurance_date}...')


def remove_from_history(
    history_file: Path,
    phrase: str,
):
    print(f'Removing {phrase} from {history_file}...')


@Gooey(
    optional_cols=2,
    program_name='Gooey subparser layout from function dict',
    program_description='Presents how to create a bundeled configuration with gooey_quick',
)
def main():
    # when passing a dict to gooey_quick.run_gooey, the keys become
    # the tabs descriptions, while the values are the function to
    # create the gui from
    gooey_quick.run_gooey({
       'Add phrase': append_to_history,
       'Remove phrase': remove_from_history,
       'Search phrases': search_history,
    })


if __name__ == '__main__':
    main()
