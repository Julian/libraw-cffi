"""
A reimplementation of https://www.libraw.org/docs/API-overview.html
"""
from unittest import TestCase

from bp.filepath import FilePath

from _raw import lib


class TestDemonstration(TestCase):
    def test_brief_demonstration(self):
        data = lib.libraw_init(0)
        self.addCleanup(lib.libraw_recycle, data)

        lib.libraw_open_file(
            data,
            FilePath(__file__).sibling("_DSC2164.ARW").path,
        )
        self.assertEqual((data.sizes.width, data.sizes.height), (5216, 3464))

        lib.libraw_unpack(data)
        lib.libraw_raw2image(data)