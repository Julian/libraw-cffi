#!/usr/bin/env python
"""
A performance benchmark using dcrawm_make_mem_image.
"""
import sys

from libraw_cffi import Raw
from libraw_cffi.tests import RADIOHEAD


def run():
    raw = Raw.from_path(RADIOHEAD)
    raw.unpack()
    raw.dcraw_process()
    processed_image = raw.dcraw_make_mem_image()


def main(runner):
    runner.bench_func("radiohead", run)


if __name__ == "__main__":
    if "--no-benchmark" in sys.argv:
        run()
    else:
        import pyperf
        main(runner=pyperf.Runner())
