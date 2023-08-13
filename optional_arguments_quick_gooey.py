from pathlib import Path
from typing import Optional

from gooey import Gooey

import gooey_quick


def upload_file(
    file: Path,
    upload_to_ftp: bool = True,
    upload_to_http: bool = False,
    backup_destination: Optional[Path] = None,
):
    destinations = []
    if upload_to_ftp:
        destinations.append('FTP')
    if upload_to_http:
        destinations.append('HTTP')
    destination = ' and '.join(destinations)

    if backup_destination:
        print(f'Uploading {file} via {destination} and backing it up at {backup_destination}')
    else:
        print(f'Uploading {file} via {destination}')


@Gooey
def main():
    gooey_quick.run_gooey(upload_file)


if __name__ == '__main__':
    main()

