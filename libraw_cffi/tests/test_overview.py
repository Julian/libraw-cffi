"""
A reimplementation of https://www.libraw.org/docs/API-overview.html
"""
from unittest import TestCase

from _raw import lib
from libraw_cffi.tests import Path


class TestDemonstration(TestCase):
    def test_brief_demonstration(self):
        data = lib.libraw_init(0)
        self.addCleanup(lib.libraw_recycle, data)

        lib.libraw_open_file(
            data,
            bytes(Path(__file__).parent / "_DSC2164.ARW"),
        )
        self.assertEqual((data.sizes.width, data.sizes.height), (5216, 3464))

        lib.libraw_unpack(data)
        lib.libraw_raw2image(data)
