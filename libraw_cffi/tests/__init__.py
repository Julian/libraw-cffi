from pathlib import Path
import os


if "RADIOHEAD" in os.environ:
    RADIOHEAD = Path(os.environ["RADIOHEAD"])
else:
    RADIOHEAD = Path(__file__).parent / "_DSC2164.ARW"
    if not RADIOHEAD.exists():
        raise RuntimeError(
            "Radiohead exists, I promise, but the test suite can't find them. "
            "Run the suite from alongsie a git checkout, or set the RADIOHEAD "
            "environment variable to the path of the _DSC2164.ARW file."
        )
RADIOHEAD_SIZE = 5216, 3464
